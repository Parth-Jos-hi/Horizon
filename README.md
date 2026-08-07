#Project
# Horizon

A personalized career forecasting tool for the job market. Upload a resume, and Horizon extracts your profile, compares it against real labor market data and forecasts, and returns a concrete path — what's declining around your current position, what's rising nearby, and what to do about it. Periodic checks surface meaningful market changes afterward, without re-uploading anything.

Full reasoning behind every decision below lives in [`docs/`](./docs) — this file is an entry point, not a substitute for those.

## Status

🔶 **In progress — Increment 1 (Core Loop).** Database layer complete (all 8 tables migrated); API schemas in progress.

| Phase | Status |
|---|---|
| Environment & Config | ✅ done |
| Database Layer | ✅ done |
| Data Ingestion Service | ⬜ not started |
| Forecasting Engine | ⬜ not started |
| Resume Intelligence Pipeline (Stages 1–4) | ⬜ not started |
| API Layer | 🔶 in progress — schemas |
| Trend Monitoring (Increment 2) | ⬜ not started |
| Conversational Agent (Increment 3) | ⬜ not started |

Detailed, file-by-file progress: [`docs/horizon-project-structure.md`](./docs/horizon-project-structure.md).

## Architecture at a Glance

```
External sources (BLS, Adzuna)  →  Data Ingestion  →  market_data_points
                                                              │
                                                              ▼
                                                        Forecasting Engine  →  forecasts
                                                              │
Resume upload  →  Extraction  →  Research Planning  →  Market Research  →  Path Synthesis
                       │                                      │                  │
                  user_profiles                        market_signals    career_paths, trend_alerts
```

Two independent flows meet at the database: a scheduled pipeline that keeps baseline market data current, and a resume-triggered pipeline that produces a personalized result. Full breakdown: [`docs/horizon-component-spec.md`](./docs/horizon-component-spec.md).

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, via SQLAlchemy 2.0 (declarative models) + Alembic (migrations)
- **Validation:** Pydantic
- **LLM:** [LLM_MODEL_PROVIDER] — resume extraction, research planning, and path synthesis
- **External data:** BLS Public Data API, Adzuna API

## Getting Started

```bash
git clone <repo-url>
cd horizon

python -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows

pip install -r requirements.txt

cp .env.example .env            # then fill in DATABASE_URL, API_KEY, JWT_SECRET_KEY

alembic upgrade head            # applies all migrations against your local Postgres

uvicorn app.main:app --reload
```

Requires a running PostgreSQL instance — connection details go in `.env`, never committed.

## Project Structure

Full file/folder layout, staged by build increment, with progress markers per file: [`docs/horizon-project-structure.md`](./docs/horizon-project-structure.md).

## Documentation

| Doc | Covers |
|---|---|
| [`horizon-project-scope.md`](./docs/horizon-project-scope.md) | Vision, features, what's explicitly out of scope, success criteria |
| [`horizon-component-spec.md`](./docs/horizon-component-spec.md) | Each service's purpose, responsibilities, and dependencies |
| [`horizon-data-model.md`](./docs/horizon-data-model.md) | Full schema, every table and column, entity relationships |
| [`horizon-implementation-guide.md`](./docs/horizon-implementation-guide.md) | Build order, phase by phase, with "done when" criteria |
| [`horizon-api-design.md`](./docs/horizon-api-design.md) | Every route, request/response shapes, FastAPI-specific notes |
| [`horizon-database-layer-process.md`](./docs/horizon-database-layer-process.md) | How and why the database layer was built, step by step |

## A Note on How This Was Built

Every component here was written by hand, not generated — the goal was full understanding of each piece, not just working output. Design decisions, including ones that changed mid-build, are preserved in the docs above rather than silently overwritten, so the reasoning stays visible.