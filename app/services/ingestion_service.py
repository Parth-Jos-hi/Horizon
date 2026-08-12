# services/ingestion_service.py
from datetime import date, datetime, timezone
from uuid import UUID
from typing import Optional

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.data_source import DataSource
from app.models.market_data_point import MarketDataPoint, MetricType


# --- BLS -----------------------------------------------------------------

# One entry per BLS series you've decided to track. Series IDs are BLS's
# own identifiers — picking the right ones for your chosen [REGION_SCOPE]
# and metrics is a real decision, not something to guess at.
BLS_SERIES = {
    "LNS14000000": MetricType.UNEMPLOYMENT_RATE,  # example: national unemployment rate
}


def fetch_bls(series_ids: list[str]) -> dict:
    response = requests.post(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        json={"seriesid": series_ids, "registrationkey": settings.BLS_API_KEY},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def map_bls_response(raw: dict) -> list[dict]:
    mapped = []
    for series in raw.get("Results", {}).get("series", []):
        metric_type = BLS_SERIES.get(series["seriesID"])
        if metric_type is None:
            continue
        for entry in series.get("data", []):
            mapped.append({
                "metric_type": metric_type,
                "region": "national",  # adjust per series if tracking sub-national data
                "sector": None,
                "role_category": None,
                "value": float(entry["value"]),
                "period_date": date(int(entry["year"]), int(entry["period"][1:]), 1),
                "raw_metadata": entry,
            })
    return mapped


# --- Adzuna ----------------------------------------------------------------

def fetch_adzuna(country: str, what: str, where: str) -> dict:
    response = requests.get(
        f"https://api.adzuna.com/v1/api/jobs/{country}/search/1",
        params={
            "app_id": settings.ADZUNA_APP_ID,
            "app_key": settings.ADZUNA_APP_KEY,
            "what": what,
            "where": where,
            "content-type": "application/json",
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def map_adzuna_response(raw: dict, region: str, role_category: str) -> list[dict]:
    # Adzuna returns individual postings, not a pre-aggregated count —
    # aggregating them into one job_postings_count row is this function's job.
    count = raw.get("count", 0)
    return [{
        "metric_type": MetricType.JOB_POSTINGS_COUNT,
        "region": region,
        "sector": None,
        "role_category": role_category,
        "value": float(count),
        "period_date": date.today().replace(day=1),
        "raw_metadata": {"mean_salary": raw.get("mean")},
    }]


# --- Persistence + orchestration -------------------------------------------

def persist_data_points(session: Session, data_source_id: UUID, rows: list[dict]) -> int:
    for row in rows:
        session.add(MarketDataPoint(data_source_id=data_source_id, **row))
    session.commit()
    return len(rows)


def _get_or_create_source(session: Session, name: str, source_type: str) -> DataSource:
    source = session.execute(
        select(DataSource).where(DataSource.name == name)
    ).scalar_one_or_none()
    if source is None:
        source = DataSource(name=name, source_type=source_type)
        session.add(source)
        session.commit()
        session.refresh(source)
    return source


def run_ingestion(session: Session) -> None:
    bls_source = _get_or_create_source(session, "BLS Public Data API", "api")
    try:
        raw = fetch_bls(list(BLS_SERIES.keys()))
        rows = map_bls_response(raw)
        persist_data_points(session, bls_source.id, rows)
        bls_source.last_synced_at = datetime.now(timezone.utc)
        session.commit()
    except requests.RequestException as e:
        print(f"BLS ingestion failed: {e}")  # replace with real logging later

    adzuna_source = _get_or_create_source(session, "Adzuna API", "api")
    try:
        raw = fetch_adzuna(country="us", what="data analyst", where="austin")
        rows = map_adzuna_response(raw, region="Austin, TX", role_category="data_analyst")
        persist_data_points(session, adzuna_source.id, rows)
        adzuna_source.last_synced_at = datetime.now(timezone.utc)
        session.commit()
    except requests.RequestException as e:
        print(f"Adzuna ingestion failed: {e}")