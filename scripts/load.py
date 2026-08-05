import psycopg2
from psycopg2.extras import execute_values
from config import *
import pandas as pd

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# ==============================
# Helper: autocast DataFrame
# ==============================
def autocast_dim(df, col_types):
    df = df.copy()
    for col, typ in col_types.items():
        if col in df.columns:
            if typ == int:
                df[col] = df[col].astype(int)
            elif typ == float:
                df[col] = df[col].astype(float)
            elif typ == str:
                df[col] = df[col].astype(str)
            elif typ == 'datetime':
                df[col] = pd.to_datetime(df[col])
    return df

# ==============================
# Load dim_customer
# ==============================
def load_dim_customer(df):
    df = autocast_dim(df, {'customer_id': int, 'first_name': str, 'last_name': str})
    print("Loading dim_customer...")
    print("Rows:", len(df))
    print(df.head())

    rows = [tuple(x) for x in df.to_numpy()]
    if rows:
        print("Sample row:", rows[0])

    query = f"""
        INSERT INTO {DWH_SCHEMA}.{DIM_CUSTOMER} (customer_id, first_name, last_name)
        VALUES %s
        ON CONFLICT (customer_id) DO NOTHING
    """

    conn = get_connection()
    cur = conn.cursor()
    execute_values(cur, query, rows)
    conn.commit()
    print("dim_customer committed.\n")
    cur.close()
    conn.close()

# ==============================
# Load dim_product
# ==============================
def load_dim_product(df):
    df = autocast_dim(df, {'product_id': int, 'product_name': str, 'product_category': str})
    print("Loading dim_product...")
    print("Rows:", len(df))
    print(df.head())

    rows = [tuple(x) for x in df.to_numpy()]
    if rows:
        print("Sample row:", rows[0])

    query = f"""
        INSERT INTO {DWH_SCHEMA}.{DIM_PRODUCT} (product_id, product_name, product_category)
        VALUES %s
        ON CONFLICT (product_id) DO NOTHING
    """

    conn = get_connection()
    cur = conn.cursor()
    execute_values(cur, query, rows)
    conn.commit()
    print("dim_product committed.\n")
    cur.close()
    conn.close()

# ==============================
# Load dim_store
# ==============================
def load_dim_store(df):
    df = autocast_dim(df, {'store_id': int, 'store_city': str})
    print("Loading dim_store...")
    print("Rows:", len(df))
    print(df.head())

    rows = [tuple(x) for x in df.to_numpy()]
    if rows:
        print("Sample row:", rows[0])

    query = f"""
        INSERT INTO {DWH_SCHEMA}.{DIM_STORE} (store_id, store_city)
        VALUES %s
        ON CONFLICT (store_id) DO NOTHING
    """

    conn = get_connection()
    cur = conn.cursor()
    execute_values(cur, query, rows)
    conn.commit()
    print("dim_store committed.\n")
    cur.close()
    conn.close()

# ==============================
# Load dim_date
# ==============================
def load_dim_date(df):
    df = autocast_dim(df, {'sales_date': 'datetime', 'year': int, 'month': int, 'day': int, 'hour': int})
    print("Loading dim_date...")
    print("Rows:", len(df))
    print(df.head())

    rows = [tuple(x) for x in df.to_numpy()]
    if rows:
        print("Sample row:", rows[0])

    query = f"""
        INSERT INTO {DWH_SCHEMA}.{DIM_DATE} (sales_date, year, month, day, hour)
        VALUES %s
        ON CONFLICT (sales_date) DO NOTHING
    """

    conn = get_connection()
    cur = conn.cursor()
    execute_values(cur, query, rows)
    conn.commit()
    print("dim_date committed.\n")
    cur.close()
    conn.close()

# ==============================
# Load fact_sales
# ==============================
def load_fact_sales(df):
    df = autocast_dim(df, {
        'sales_id': int,
        'transaction_number': str,
        'sales_date': 'datetime',
        'store_id': int,
        'customer_id': int,
        'product_id': int,
        'price': float,
        'quantity': int,
        'discount': float,
        'sales': float
    })

    print("Loading fact_sales...")
    print("Rows:", len(df))
    print(df.head())

    rows = [tuple(x) for x in df.to_numpy()]
    if rows:
        print("Sample row:", rows[0])

    query = f"""
        INSERT INTO {DWH_SCHEMA}.{FACT_SALES}
        (sales_id, transaction_number, sales_date, store_id, customer_id, product_id, price, quantity, discount, sales)
        VALUES %s
        ON CONFLICT (sales_id, sales_date) DO NOTHING
    """

    conn = get_connection()
    cur = conn.cursor()
    execute_values(cur, query, rows)
    conn.commit()
    print("fact_sales committed.\n")
    cur.close()
    conn.close()