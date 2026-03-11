# netflix_dbt

Local dbt + Snowflake project for Netflix titles/credits analytics.

## What this project does

1. Loads raw CSV data (`datasets/titles.csv`, `datasets/credits.csv`) into Snowflake raw schema (`DBT_RAW` by default).
2. Builds stage, dimension, and fact models in Snowflake via dbt.
3. Runs model/data tests.
4. Generates dbt docs artifacts.

## Project layout

```text
netflix_dbt/
  datasets/
    data_load.py
    titles.csv
    credits.csv
  models/netflix/stage/
    src_netflix.yml
    stage_netflix.yml
    SHOW_DETAILS_DIM.sql
    SCORES_VOTES_DIM.sql
    CREDITS_DIM.sql
  models/netflix/dimension/
    POPULARITY_DIM.sql
  models/netflix/fact/
    MOVIES_SERIES_SHARE.sql
    ACTORS_DOMINATING_FACT.sql
    fact_netflix.yml
  run_pipeline.sh
  dbt_project.yml
```

## Prerequisites

1. Python virtual environment at `../.venv` with packages:
   - `dbt-snowflake`
   - `snowflake-connector-python`
   - `pandas`
   - `python-dotenv`
2. Snowflake account, user, role, warehouse, and database.
3. `profiles.yml` available in `.dbt_profiles/` (local only, not committed).

## Local configuration

### 1) Environment variables for raw loader

Create `netflix_dbt/.env`:

```env
SNOWFLAKE_ACCOUNT=<account_locator>
SNOWFLAKE_USER=<username>
SNOWFLAKE_PASSWORD=<password>
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=PROD
SNOWFLAKE_RAW_SCHEMA=DBT_RAW
```

### 2) dbt profile

Use `.dbt_profiles/profiles.example.yml` as a template and create `.dbt_profiles/profiles.yml`.

Expected profile key must match `dbt_project.yml`:

```yaml
profile: 'netflix_dbt'
```

You can run dbt either with:

```bash
dbt run --profiles-dir .dbt_profiles
```

or export once per shell:

```bash
export DBT_PROFILES_DIR="$PWD/.dbt_profiles"
```

## Run commands

### Option A: full pipeline script

```bash
cd ~/OneDrive/Documents/WorkSpace/dbt-snowflake-project/netflix_dbt
./run_pipeline.sh
```

### Option B: step-by-step

```bash
cd ~/OneDrive/Documents/WorkSpace/dbt-snowflake-project/netflix_dbt
../.venv/Scripts/python.exe datasets/data_load.py
../.venv/Scripts/dbt.exe run --select models/netflix --profiles-dir .dbt_profiles
../.venv/Scripts/dbt.exe test --select models/netflix --profiles-dir .dbt_profiles
../.venv/Scripts/dbt.exe docs generate --profiles-dir .dbt_profiles
```

## Model groups

1. `stage`:
   - `SHOW_DETAILS_DIM`
   - `SCORES_VOTES_DIM`
   - `CREDITS_DIM`
2. `dimension`:
   - `POPULARITY_DIM`
3. `fact`:
   - `MOVIES_SERIES_SHARE`
   - `ACTORS_DOMINATING_FACT`

## Common issues

1. `Could not find profile named 'netflix_dbt'`
   - Ensure `.dbt_profiles/profiles.yml` exists.
   - Ensure top-level key is `netflix_dbt`.
   - Run with `--profiles-dir .dbt_profiles` or export `DBT_PROFILES_DIR`.

2. `Role 'TEST_DBT_ROLE' does not exist or not authorized`
   - Remove or update any model `post_hook` grants that reference `TEST_DBT_ROLE`.

3. `invalid identifier 'ID'` during raw load
   - Caused by old quoted/lowercase table columns in Snowflake.
   - Loader drops and recreates `TITLES` and `CREDITS` to avoid casing drift.

## Security notes

1. Do not commit `.env` or `.dbt_profiles/profiles.yml`.
2. Use `.dbt_profiles/profiles.example.yml` as the only committed profile reference.
