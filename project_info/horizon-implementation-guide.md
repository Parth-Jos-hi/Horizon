# Horizon — Implementation Guide

> **Revised.** Phases 4–5 (old Profile Service + Career Path Engine) are now four phases, one per pipeline stage, plus a new phase for the recurring trend-monitoring check.

## Phase 0 — Environment & Config ✅ done

`app/config.py` centralizing settings from environment variables.

## Phase 1 — Database Layer 🔶 in progress

Model order: `users` → `data_sources` → `market_data_points` → `forecasts` → `user_profiles` → `market_signals` (NEW) → `career_paths` → `trend_alerts` (NEW) → `agent_sessions` → `agent_interactions` → `agent_tools`.

**Status:** `base.py` ✅ · `session.py` ✅ · `user.py` ✅ · `data_source.py` ✅ · `market_data_point.py` ✅ · `forecast.py` ← current. `user_profile.py`, `market_signal.py`, `career_path.py`, `trend_alert.py`, and the remaining agent tables are not yet started.

**Done when:** every table in the current data model exists in Postgres via a reviewed migration.

## Phase 2 — Data Ingestion Service ⬜

Fetch from BLS and Adzuna, map onto `market_data_points`, update `data_sources.last_synced_at`.

**Done when:** one real run against each source populates verifiable rows.

## Phase 3 — Forecasting Engine ⬜

Given a metric/region/sector/role/horizon combination, read `market_data_points`, apply [FORECASTING_METHOD], write to `forecasts`.

**Done when:** one real forecast is generated with an accurate recorded historical window.

## Phase 4 — Resume Pipeline, Stage 1: Extraction Agent ⬜

Accept resume upload, extract text, use [LLM_MODEL_PROVIDER] to extract structured fields, write to `user_profiles`.

**Done when:** a real resume produces a `user_profiles` row with an accurate `field` and `region`.

## Phase 5 — Resume Pipeline, Stage 2: Research Planner Agent ⬜

Take a `user_profiles` row, produce a research plan — concrete search targets covering the person's role, adjacent roles, and related skills. Log the plan via `agent_interactions.tool_calls`.

**Done when:** given a real profile, the plan produced is something you could hand to a person and have them go research the right things.

## Phase 6 — Resume Pipeline, Stage 3: Market Research Agent ⬜

Execute the research plan using a real web search tool, write one `market_signals` row per relevant finding.

**Done when:** a real research plan produces `market_signals` rows with real, checkable `source_url` values.

**Depends on:** the web search tool decision from the open-decisions list — this phase can't start meaningfully until that's picked.

## Phase 7 — Resume Pipeline, Stage 4: Path Synthesis Agent ⬜

Read `market_data_points`/`forecasts` (via the Forecasting Engine) and `market_signals` for a profile, produce `declining_signals`/`rising_signals`/`recommended_path`, write to `career_paths`. Separately, evaluate whether the result is significant enough to also write a `trend_alerts` row.

**Done when:** a real profile produces a `career_paths` row fully traceable to real `forecasts` and `market_signals` rows, and the significance check correctly withholds a `trend_alerts` row when nothing meaningful changed.

**Note:** this is the phase most worth slowing down on — both the gap-analysis logic and the significance threshold are the actual product, not formalities.

## Phase 8 — Recurring Trend Monitoring ⬜

A scheduled job (independent of new uploads) that re-runs Stage 4's significance check against existing profiles, so a user gets alerts over time without re-uploading.

**Done when:** running this job against a profile with genuinely new `market_signals` since the last check produces a correct `trend_alerts` row, and running it again immediately after produces none.

## Phase 9 — API Layer ⬜

`/auth`, `/user`, `/data`, `/forecasts`, `/profile` (triggers the pipeline), `/career-path`, `/trend-alerts` routes using [API_FRAMEWORK].

**Done when:** the full upload → extract → plan → research → synthesize sequence is exercisable end to end with `curl`/Postman, no agent or frontend involved.

## Phase 10 — Conversational Agent Service ⬜

`agent_tools` registry, context assembly, orchestration loop, `/agent/query` route.

**Done when:** a follow-up question about an existing `career_paths` or `trend_alerts` result is answered correctly using that specific result.

## Phase 11 — Testing & Validation ⬜

Automated tests per service/stage, including a full scripted end-to-end resume-to-path-to-alert test.

## Phase 12 — Deployment ⬜

Containerize, deploy, schedule both the ingestion job (Phase 2) and the trend-monitoring job (Phase 8).

## Cross-Cutting Notes

- Each phase depends on the one before it actually working. Phase 7 in particular should not be attempted against unverified Phase 6 output.
- Every placeholder needs resolving before its corresponding phase, not before the project starts. The web search tool decision (Phase 6) and the significance threshold (Phase 7) are the two most consequential ones left.
