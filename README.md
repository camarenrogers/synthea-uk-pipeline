# Synthetic Patient Data Pipeline (UK)

An end-to-end data engineering pipeline that generates synthetic UK
healthcare records with Synthea, loads them into a DuckDB warehouse,
and transforms them into clean, tested, analysis-ready tables with dbt.

## Architecture

Synthea (UK config) → CSV → DuckDB (raw schema) → dbt (staging → marts)

- **Generation** — Synthea International, configured for Great Britain
  (Somerset / Bristol), exporting FHIR and CSV.
- **Loading** — a Python script loads all raw CSVs into DuckDB under a
  `raw` schema.
- **Transformation** — dbt models clean and rename the raw data
  (staging layer), then build analytical marts.
- **Testing** — dbt data tests enforce uniqueness, non-null keys, and
  referential integrity between models.

## Data models

**Staging** (one model per source, cleaned & renamed):
`stg_patients`, `stg_encounters`, `stg_conditions`,
`stg_observations`, `stg_medications`

**Marts** (analysis-ready):
- `patient_summary` — one row per patient with demographics, age, and
  encounter statistics
- `condition_prevalence` — conditions ranked by number of distinct
  patients affected

## Tech stack

Synthea · Python · DuckDB · dbt · SQL

## How to run

1. Generate data with Synthea (UK config) into `output/csv/`.
2. Load into DuckDB: `python load_raw.py`
3. Build and test the pipeline:
