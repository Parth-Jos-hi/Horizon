# Horizon — Project Scope

> **Revised.** The resume-to-path flow is now explicitly a 4-stage agent pipeline (extract → plan → research → synthesize), and periodic trend monitoring is a first-class feature, not an afterthought.

## Vision

Horizon is a personalized career forecasting tool. A user logs in, uploads their resume, and a four-stage agent pipeline extracts their professional profile, plans what's worth researching about their field, actively searches current sources for relevant market signals, and synthesizes all of it — alongside structured labor market data — into a concrete path: what's declining around their current position, what's rising nearby, and what to do about it. After that first analysis, Horizon continues to watch for meaningful changes and surfaces them periodically — not on a fixed daily cadence, but when there's actually something worth reporting.

## Problem Statement

Job seekers know their own resume but not where their field is actually headed, and market conditions keep changing after the first time they check. Horizon closes both gaps: a personalized analysis grounded in real research the first time, and ongoing, meaningful (not noisy) updates after that.

## Target Users

- Job seekers wanting to know if their current path is trending up or down, and what to do about it
- Career changers evaluating whether a pivot is supported by real market direction
- [ADDITIONAL_USER_SEGMENT]

## Core MVP Features

1. Login/register and account management
2. Resume upload, processed by a 4-stage agent pipeline:
   - Extraction — structured profile from raw resume text
   - Research planning — deciding what's actually worth investigating for this profile
   - Market research — live web search for current, profile-relevant signals
   - Synthesis — gap analysis, recommended path, and (when warranted) a trend alert
3. Baseline structured market data (BLS + Adzuna), ingested on a schedule, independent of any single user — the quantitative backbone the synthesis stage draws on alongside live research
4. Forecast generation from that baseline data
5. Periodic, trend-triggered updates — "here's what changed in your market" — sent only when the research/monitoring process finds something genuinely significant, not on a fixed schedule
6. A conversational agent for follow-up questions about a generated path or alert, or general market questions

## Out of Scope for v1

- Real-time/streaming baseline data ingestion — periodic batch is sufficient
- Parsing scanned/image-based resumes (OCR) — text-based PDF/DOCX only
- Matching a user to specific live job postings — Horizon shows market direction, not a job board
- Comparing multiple resumes against each other
- Multi-language support
- A dedicated mobile app
- Paid tiers / billing
- Guaranteeing a fixed alert frequency (e.g. "weekly, always") — frequency is signal-driven, by design, not calendar-driven

## Success Criteria

- A real resume, uploaded end to end, produces a gap analysis traceable to both real `forecasts` and real, cited `market_signals` — not a generic or hallucinated response
- At least one `trend_alerts` row is correctly generated (and correctly *not* generated when there's nothing significant) during testing
- The agent correctly answers a defined set of representative follow-up questions about a generated path
- All pipeline stages complete within a latency acceptable for the flow (upload does not need to feel instant, but should not feel broken)
- At least one full baseline ingestion cycle runs end-to-end against BLS and Adzuna

## Assumptions & Constraints

- BLS Public Data API and Adzuna API are the baseline `[DATA_SOURCE_PROVIDER(S)]` — see `horizon-data-model.md` for what each covers
- The Market Research Agent needs an actual web search capability — a decision on which tool/API this is, and which sites are in scope, is still open
- Resume parsing/extraction and path synthesis both use [LLM_MODEL_PROVIDER]
- v1 forecasting can be a relatively simple method (e.g. trend extrapolation)
- Single-tenant for v1
- Geographic scope for v1: [REGION_SCOPE]
- "Nearby" rising roles/skills and "significant enough for a trend alert" both need explicit, defensible definitions — these are the actual core logic of the product

## Phases (High-Level)

1. **Data model + baseline ingestion** — schema in place, BLS + Adzuna flowing into `market_data_points`
2. **Forecasting** — basic forecast generation from baseline data
3. **Resume Intelligence Pipeline** — all four stages, in order, building on phases 1–2
4. **API layer** — every route above exercisable without a frontend or agent
5. **Conversational agent** — natural-language follow-up over pipeline outputs, plus general market Q&A
6. **Refinement** — additional data sources, better forecasting and significance-detection methods, richer trend alerts over time

## Open Decisions

- [ ] Web search tool/API for the Market Research Agent, and which sites are in scope
- [ ] Significance threshold for a `trend_alerts` row
- [ ] How the recurring significance-check (for existing profiles, without a new upload) is scheduled
- [ ] What counts as a "nearby" rising role/skill
- [ ] Resume file formats supported for v1
- [ ] Whether extracted profile data needs user confirmation before the pipeline continues
