import pandas as pd
import psycopg2
from extract import extract_data
from transform import (
    transform_dim_customer,
    transform_dim_product,
    transform_dim_store,
    transform_dim_date,
    transform_fact_sales
)
from load import (
    load_dim_customer,
    load_dim_product,
    load_dim_store,
    load_dim_date,
    load_fact_sales
)
from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DWH_SCHEMA,
    FACT_SALES
)

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def get_last_sales_date():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT MAX(sales_date)
        FROM {DWH_SCHEMA}.{FACT_SALES}
    """)

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return pd.to_datetime(result) if result else pd.Timestamp("1900-01-01")

def run_delta_load():
    print("Starting Delta Load...")

    # Ambil last date dari database
    last_date = get_last_sales_date()
    print(f"Last sales_date in fact_sales: {last_date}")

    # Extract full raw data
    df_raw = extract_data()
    df_raw["sales_date"] = pd.to_datetime(
        df_raw["sales_date"],
        format="mixed",
        errors="coerce"
    )

    # Filter hanya data baru
    df_new = df_raw[df_raw["sales_date"] > last_date].copy()

    if df_new.empty:
        print("No new data to load.")
        return

    print(f"New rows found: {len(df_new)}")

    # Transform
    dim_customer = transform_dim_customer(df_new)
    dim_product = transform_dim_product(df_new)
    dim_store = transform_dim_store(df_new)
    dim_date = transform_dim_date(df_new)
    fact_sales = transform_fact_sales(df_new)

    # Load
    load_dim_customer(dim_customer)
    load_dim_product(dim_product)
    load_dim_store(dim_store)
    load_dim_date(dim_date)
    load_fact_sales(fact_sales)

    print("Delta Load Completed!")

if __name__ == "__main__":
    run_delta_load()