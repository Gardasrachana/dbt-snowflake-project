#!/usr/bin/env bash
set -euo pipefail
 
cd "$(dirname "$0")"
if [[ -f ../.venv/Scripts/activate ]]; then
  # Git Bash on Windows virtualenv layout
  source ../.venv/Scripts/activate
elif [[ -f ../.venv/bin/activate ]]; then
  # Linux/macOS virtualenv layout
  source ../.venv/bin/activate
else
  echo "Could not find virtualenv activate script at ../.venv/{Scripts,bin}/activate"
  exit 1
fi
export DBT_PROFILES_DIR="$PWD/.dbt_profiles"
 
echo "1) Loading CSVs to Snowflake RAW..."
python datasets/data_load.py
 
echo "2) Building + testing Netflix models..."
dbt build --select models/netflix
 
echo "3) Generating dbt docs..."
dbt docs generate
 
echo "Done."
