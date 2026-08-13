# services/pipeline/path_synthesis_agent.py
import json
from typing import Optional

from pydantic import BaseModel, ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile
from app.models.market_signal import MarketSignal
from app.models.forecast import Forecast
from app.models.career_path import CareerPath
from app.models.trend_alert import TrendAlert
from app.services.forecasting_service import get_historical_window
from app.services.agent.llm_client import generate_text

SYNTHESIS_SYSTEM_PROMPT = """Given declining and rising market signals for a
person's profile, write a concrete, specific recommended path — guide through the path that where and how to improve
, no generic advice. Respond with ONLY valid JSON:
{"recommended_path": str}"""

SIGNIFICANCE_MIN_AGREEING_SIGNALS = 5


class SynthesisOutput(BaseModel):
    recommended_path: str


def _pct_change_vs_latest_actual(forecast: Forecast, session: Session) -> float:
    history = get_historical_window(
        session, forecast.metric_type, forecast.region, forecast.sector, forecast.role_category
    )
    if not history or history[-1].value == 0:
        return 0.0
    latest_actual = history[-1].value
    return (forecast.predicted_value - latest_actual) / latest_actual


def identify_signals(
    session: Session, profile: UserProfile, forecasts: list[Forecast]
) -> tuple[list[dict], list[dict]]:
    """First-pass 'nearby' rule, NOT the final answer — horizon-data-model.md
    still flags this as an open decision. Current rule: the user's own
    role_category trending down = declining; any OTHER role_category in the
    same region trending up = rising."""
    declining, rising = [], []
    for f in forecasts:
        change = _pct_change_vs_latest_actual(f, session)
        entry = {
            "role_category": f.role_category,
            "region": f.region,
            "pct_change": round(change * 100, 1),
        }
        if f.role_category == profile.current_role and change < 0:
            declining.append(entry)
        elif f.role_category != profile.current_role and change > 0:
            rising.append(entry)
    return declining, rising


def compose_recommended_path(declining: list[dict], rising: list[dict]) -> str:
    prompt = f"Declining: {json.dumps(declining)}\nRising: {json.dumps(rising)}"
    response = generate_text(prompt=prompt, system=SYNTHESIS_SYSTEM_PROMPT)
    try:
        return SynthesisOutput.model_validate(json.loads(response)).recommended_path
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Synthesis did not return valid structured data: {e}")


def check_significance(new_signals: list[MarketSignal]) -> Optional[str]:
    if len(new_signals) >= SIGNIFICANCE_MIN_AGREEING_SIGNALS:
        return f"{len(new_signals)} new market signals found since last check"
    return None


def run_synthesis(
    session: Session,
    profile: UserProfile,
    new_signals: list[MarketSignal],
    forecasts: list[Forecast],
) -> tuple[CareerPath, Optional[TrendAlert]]:
    declining, rising = identify_signals(session, profile, forecasts)
    recommended_path = compose_recommended_path(declining, rising)

    career_path = CareerPath(
        user_id=profile.user_id,
        profile_id=profile.id,
        declining_signals=declining,
        rising_signals=rising,
        recommended_path=recommended_path,
        based_on_forecast_ids=[str(f.id) for f in forecasts],
        based_on_signal_ids=[str(s.id) for s in new_signals],
    )
    session.add(career_path)

    trend_alert = None
    reason = check_significance(new_signals)
    if reason is not None:
        trend_alert = TrendAlert(
            user_id=profile.user_id,
            profile_id=profile.id,
            summary=recommended_path,
            based_on_signal_ids=[str(s.id) for s in new_signals],
            triggered_reason=reason,
        )
        session.add(trend_alert)

    session.commit()
    session.refresh(career_path)
    return career_path, trend_alert