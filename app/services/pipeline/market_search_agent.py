# services/pipeline/market_research_agent.py
#
# INCOMPLETE BY NECESSITY — blocked on the open web search tool/API
# decision in horizon-data-model.md. search_web() below defines the
# interface every other stage expects; it has no real implementation
# yet. Options worth choosing between: Tavily API, Serper, a
# search-capable tool from your [LLM_MODEL_PROVIDER], Google Custom
# Search. Pick one, then implement this function — nothing else in
# this file changes once you do.

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.market_signal import MarketSignal
from app.services.pipeline.research_planner_agent import ResearchPlan


def search_web(query: str) -> list[dict]:
    """Should return [{"url": str, "snippet": str}, ...]."""
    raise NotImplementedError("Choose a web search tool before implementing this")


def run_market_research(
    session: Session, profile_id: UUID, plan: ResearchPlan
) -> list[MarketSignal]:
    signals = []
    for query in plan.queries:
        for result in search_web(query):
            signal = MarketSignal(
                profile_id=profile_id,
                query=query,
                source_url=result["url"],
                summary=result["snippet"],
            )
            session.add(signal)
            signals.append(signal)
    session.commit()
    return signals