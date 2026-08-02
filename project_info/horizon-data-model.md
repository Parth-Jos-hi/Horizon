# Horizon — Data Model

> **Revised.** Adds `market_signals` and `trend_alerts` to support the 4-stage resume research pipeline. All previously existing entities are unchanged.

## Entities

### `users`

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `email` | string, unique | |
| `password_hash` | string | |
| `display_name` | string | |
| `role` | enum(`user`, `admin`) | |
| `created_at` / `updated_at` | timestamp | |

### `data_sources`

Baseline, scheduled, structured sources — currently BLS and Adzuna.

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `name` | string | e.g. "BLS Public Data API", "Adzuna API" |
| `source_type` | enum(`api`, `csv_upload`, `scraper`) | |
| `reference_url` | string, nullable | |
| `last_synced_at` | timestamp, nullable | |
| `enabled` | boolean, default true | |
| `created_at` | timestamp | |

### `market_data_points`

Structured, dimensioned metrics from the scheduled ingestion pipeline. Unchanged.

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `data_source_id` | UUID (FK → `data_sources.id`) | |
| `metric_type` | enum(`job_postings_count`, `avg_salary`, `unemployment_rate`, `sector_growth_rate`, ...) | |
| `region` | string | |
| `sector` | string, nullable | |
| `role_category` | string, nullable | |
| `value` | numeric | |
| `period_date` | date | |
| `ingested_at` | timestamp | |
| `raw_metadata` | JSON, nullable | |

### `forecasts`

Unchanged.

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `requested_by_user_id` | UUID (FK → `users.id`), nullable | |
| `metric_type` | enum, same set as `market_data_points` | |
| `region` / `sector` / `role_category` | string (nullable where applicable) | |
| `horizon` | enum(`1_month`, `3_month`, `1_year`) | |
| `predicted_value` | numeric | |
| `confidence_low` / `confidence_high` | numeric, nullable | |
| `method` | string | e.g. "[FORECASTING_METHOD]" |
| `based_on_period_start` / `based_on_period_end` | date | |
| `created_at` | timestamp | |

### `user_profiles`

Output of Stage 1 (Extraction Agent). Unchanged.

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `user_id` | UUID (FK → `users.id`) | |
| `source_filename` | string, nullable | |
| `original_file_storage_key` | string, nullable | |
| `raw_text` | text | |
| `current_role` | string, nullable | |
| `field` | string | |
| `region` | string | |
| `skills` | JSON | |
| `years_experience` | numeric, nullable | |
| `uploaded_at` | timestamp | |
| `parsed_at` | timestamp, nullable | |

### `market_signals` — NEW

Output of Stage 3 (Market Research Agent). Live, messier, web-sourced findings — distinct from the clean, dimensioned `market_data_points`.

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `profile_id` | UUID (FK → `user_profiles.id`) | which resume's research this came from |
| `query` | string | what Stage 2 (Research Planner Agent) told Stage 3 to look for |
| `source_url` | string | where this finding came from |
| `summary` | text | what the agent extracted from that source |
| `relevance` | string, nullable | lightweight tag — e.g. "skill_demand_rising", "role_declining", "general_news" |
| `discovered_at` | timestamp | |

### `career_paths`

Output of Stage 4 (Path Synthesis Agent). `based_on_forecast_ids` extended conceptually to also draw on `market_signals`, not just `forecasts`.

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `user_id` | UUID (FK → `users.id`) | |
| `profile_id` | UUID (FK → `user_profiles.id`) | |
| `declining_signals` | JSON | |
| `rising_signals` | JSON | |
| `recommended_path` | text | |
| `based_on_forecast_ids` | JSON | array of `forecasts.id` |
| `based_on_signal_ids` | JSON | array of `market_signals.id` — NEW column |
| `generated_at` | timestamp | |

### `trend_alerts` — NEW

Also produced by Stage 4, but on its own trigger — not every generation of a `career_paths` row produces one of these. Only created when Stage 4 judges there's a meaningful, new change worth telling the user about.

| Column | Type | Description |
|---|---|---|
| `id` | UUID (PK) | |
| `user_id` | UUID (FK → `users.id`) | |
| `profile_id` | UUID (FK → `user_profiles.id`) | |
| `summary` | text | the actual "here's what changed" message |
| `based_on_signal_ids` | JSON | array of `market_signals.id` this alert is traceable to |
| `triggered_reason` | text, nullable | why this fired now, in plain language |
| `created_at` | timestamp | |

### `agent_sessions`

Unchanged.

### `agent_interactions`

Unchanged. Also where Stage 2's research plan gets logged, via `tool_calls`, rather than a dedicated table.

### `agent_tools`

Registry now includes entries for each pipeline stage's capability — e.g. `extract_resume`, `plan_research`, `web_search`, `query_market_data`, `generate_forecast`, `generate_career_path`, `check_trend_significance`.

## Entity Relationships

- `user_profiles` → `market_signals` (one profile triggers many research findings)
- `market_signals` → `career_paths` and `trend_alerts` (both traceable back to the signals that informed them)
- `data_sources` → `market_data_points` → `forecasts` chain (baseline pipeline) unchanged, and still feeds `career_paths` alongside `market_signals`

## Open Decisions

- [ ] What tool/API the Market Research Agent actually uses to search (a web search API, restricted to specific job/news sites, respecting each site's terms of service)
- [ ] The significance threshold for creating a `trend_alerts` row — how many/what kind of new `market_signals` justify one
- [ ] How often Stage 4 checks for alert-worthiness (a recurring job, separate from the on-upload pipeline run)
- [ ] Whether `market_signals` should ever be deduplicated/shared across users in the same field+region, rather than always being profile-specific
- [ ] Full `metric_type` enum, [DATABASE_TYPE], [FILE_STORAGE_PROVIDER] — carried over, still open
