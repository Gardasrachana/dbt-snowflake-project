import os
from pathlib import Path
import pandas as pd
import snowflake.connector as snow
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
 
load_dotenv()
 
def get_conn():
    return snow.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
    )
 
def main():
    raw_schema = os.getenv("SNOWFLAKE_RAW_SCHEMA", "DBT_RAW")
    base = Path(__file__).resolve().parent
 
    titles_df = pd.read_csv(base / "titles.csv")
    credits_df = pd.read_csv(base / "credits.csv")
 
    # Keep Snowflake column references simple (ID, TITLE, etc.)
    titles_df.columns = [c.upper() for c in titles_df.columns]
    credits_df.columns = [c.upper() for c in credits_df.columns]
 
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {raw_schema}")
        cur.execute(f"USE SCHEMA {raw_schema}")
        # Recreate tables to avoid column-name casing drift from previous loads.
        # Existing quoted lowercase columns (e.g., "id") break unquoted inserts (ID).
        cur.execute("DROP TABLE IF EXISTS TITLES")
        cur.execute("DROP TABLE IF EXISTS CREDITS")
 
        write_pandas(conn, titles_df, "TITLES", auto_create_table=True, quote_identifiers=False)
        write_pandas(conn, credits_df, "CREDITS", auto_create_table=True, quote_identifiers=False)
 
        print("Loaded TITLES and CREDITS into", raw_schema)
    finally:
        cur.close()
        conn.close()
 
if __name__ == "__main__":
    main()
