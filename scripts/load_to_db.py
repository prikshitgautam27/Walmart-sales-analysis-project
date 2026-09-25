"""
Walmart Sales Data - Load to PostgreSQL
-----------------------------------------
Loads the cleaned CSV into a PostgreSQL database.

Before running:
  1. Create a database called walmart_db in PostgreSQL
  2. Update DB_USER / DB_PASSWORD below with your own credentials
  3. pip install -r requirements.txt

Run from the project root:
    python scripts/load_to_db.py
"""

import pandas as pd
from sqlalchemy import create_engine

CLEAN_PATH = "data/walmart_clean_data.csv"

# --- Update these with your own local PostgreSQL credentials ---
DB_USER = "postgres"
DB_PASSWORD = "your_password_here"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "walmart_db"


def get_engine():
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_str)


def main():
    df = pd.read_csv(CLEAN_PATH)
    engine = get_engine()

    try:
        with engine.connect() as conn:
            print("Connected to PostgreSQL successfully")
    except Exception as e:
        print("Connection failed:", e)
        return

    df.to_sql(name="walmart", con=engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into the 'walmart' table")


if __name__ == "__main__":
    main()
