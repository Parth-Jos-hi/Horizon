# Horizon — Component Spec

> **Revised.** Components 4 and 5 from the previous version are consolidated into one 4-stage pipeline, matching the real product flow: upload → extract → plan → research → synthesize.

## 1. Auth & User Service

Unchanged. Register/authenticate users, issue/validate tokens, expose profile read/update. Depends on `users`.

---

## 2. Data Ingestion Service

Unchanged. Scheduled, structured pulls from BLS and Adzuna into `market_data_points`. Runs independently of any user action, on its own timer.

---

## 3. Forecasting Engine

Unchanged. Turns `market_data_points` into `forecasts` using [FORECASTING_METHOD].

---

## 4. Resume Intelligence Pipeline — REVISED (was Profile Service + Career Path Engine)

**Purpose:** the core of the product. Triggered once by a resume upload, runs four stages in sequence.

### Stage 1 — Extraction Agent
Reads the raw resume text, uses [LLM_MODEL_PROVIDER] to extract structured fields — current role, skills, field, region, years of experience. Writes to `user_profiles`.

### Stage 2 — Research Planner Agent
Takes the structured profile and decides what's actually worth researching — not just the literal current role, but adjacent roles, related skills, and nearby sectors worth checking for both declining and rising signals. Produces a research plan (a list of concrete search targets). Not persisted as its own table — logged via `agent_interactions.tool_calls` for traceability.

### Stage 3 — Market Research Agent
Executes the research plan using a real web search tool — this is the "patrol around the sites online" step. For each target, it searches, finds relevant current information, and writes one row per finding to `market_signals`.

### Stage 4 — Path Synthesis Agent
Reads everything available for this profile: the structured `market_data_points`/`forecasts` (calling into the Forecasting Engine if a needed forecast doesn't exist yet) and the fresh `market_signals` from Stage 3. Produces two possible outputs:
- Always: a `career_paths` row — the gap analysis and recommended path
- Sometimes: a `trend_alerts` row, only if there's a meaningful new change worth telling the user about — this is what makes updates arrive weekly/monthly rather than daily

**Depends on:** `user_profiles`, `market_signals`, `market_data_points`, `forecasts`, `career_paths`, `trend_alerts`; calls the Forecasting Engine rather than duplicating it.

**Open questions:** exact significance threshold for a `trend_alerts` row; which web search tool/API Stage 3 uses and what sites are in scope; whether Stage 4 also runs on a recurring schedule independent of new uploads, to catch changes for existing profiles.

---

## 5. Conversational Agent Service

**Purpose:** answers ad-hoc natural-language questions — both general market questions and follow-ups about an existing `career_paths` or `trend_alerts` result.

**Responsibilities:** assemble context from `agent_interactions` plus relevant `market_data_points`/`forecasts`/`career_paths`/`market_signals`; decide whether to answer directly or invoke a tool from `agent_tools`; persist every turn.

**Depends on:** `agent_sessions`, `agent_interactions`, `agent_tools`; read access across the pipeline's output tables; can call the Resume Intelligence Pipeline's stages as tools (e.g. to re-trigger research) rather than duplicating their logic.

**Distinction worth being precise about in an interview:** this service reacts to a user typing a question. The Resume Intelligence Pipeline reacts to a resume upload (or a scheduled significance check). Different triggers, different jobs — even though both are "agents" in the general sense.

---

## 6. API Layer

**Purpose:** single entry point for every client.

**Responsibilities:** expose auth/user, data, forecast, profile (upload trigger for the pipeline), career-path, trend-alert, and agent endpoints; rate-limit the expensive routes (pipeline trigger, agent query, forecast generation).

**Depends on:** all components above.

## Component Interaction (Read Order)

**Resume upload flow:** **API Layer** (`/profile/upload`) → **Resume Intelligence Pipeline** runs Stages 1–4 in sequence → `user_profiles`, `market_signals`, `career_paths` written, `trend_alerts` written only if warranted → result returned through the **API Layer**.

**Ongoing monitoring:** Stage 4 also runs on its own recurring check (independent of new uploads) against existing profiles, so a user who uploaded once can still receive a `trend_alerts` row weeks later without re-uploading.

**Conversational follow-up flow:** **API Layer** (`/agent/query`) → **Conversational Agent Service** reads from the pipeline's output tables for grounding, optionally calls pipeline stages as tools → response persisted → returned.

**Data Ingestion Service** runs independently of everything above, on its own schedule.
