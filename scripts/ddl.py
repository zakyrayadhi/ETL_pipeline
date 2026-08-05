import psycopg2
from datetime import datetime, timedelta
from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DWH_SCHEMA,
    DM_SCHEMA,
    DIM_CUSTOMER,
    DIM_PRODUCT,
    DIM_STORE,
    DIM_DATE,
    FACT_SALES,
    DM_SUMMARY_SALES_PER_HOUR,
    DM_SUMMARY_PRODUCT_SALES,
    DM_SUMMARY_STORE_SALES,
    DM_SUMMARY_DAILY_SALES
)


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# =========================
# DROP ALL TABLES (AMAN)
# =========================
def drop_all_tables(confirm=False):
    if not confirm:
        print("Drop dibatalkan. Gunakan drop_all_tables(confirm=True) kalau yakin.")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Drop datamart tables dulu
        cur.execute(f"DROP TABLE IF EXISTS {DM_SCHEMA}.{DM_SUMMARY_SALES_PER_HOUR} CASCADE;")
        cur.execute(f"DROP TABLE IF EXISTS {DM_SCHEMA}.{DM_SUMMARY_PRODUCT_SALES} CASCADE;")
        cur.execute(f"DROP TABLE IF EXISTS {DM_SCHEMA}.{DM_SUMMARY_STORE_SALES} CASCADE;")
        cur.execute(f"DROP TABLE IF EXISTS {DM_SCHEMA}.{DM_SUMMARY_DAILY_SALES} CASCADE;")

        # Drop fact partitions dulu (kalau ada)
        cur.execute(f"""
            DO $$
            DECLARE
                part RECORD;
            BEGIN
                FOR part IN
                    SELECT tablename
                    FROM pg_tables
                    WHERE schemaname = '{DWH_SCHEMA}'
                      AND tablename LIKE '{FACT_SALES}_%'
                LOOP
                    EXECUTE 'DROP TABLE IF EXISTS {DWH_SCHEMA}.' || part.tablename || ' CASCADE';
                END LOOP;
            END $$;
        """)

        # Drop parent fact table
        cur.execute(f"DROP TABLE IF EXISTS {DWH_SCHEMA}.{FACT_SALES} CASCADE;")

        # Drop dim tables
        cur.execute(f"DROP TABLE IF EXISTS {DWH_SCHEMA}.{DIM_DATE} CASCADE;")
        cur.execute(f"DROP TABLE IF EXISTS {DWH_SCHEMA}.{DIM_STORE} CASCADE;")
        cur.execute(f"DROP TABLE IF EXISTS {DWH_SCHEMA}.{DIM_PRODUCT} CASCADE;")
        cur.execute(f"DROP TABLE IF EXISTS {DWH_SCHEMA}.{DIM_CUSTOMER} CASCADE;")

        conn.commit()
        print("Semua tabel berhasil di-drop.")

    except Exception as e:
        conn.rollback()
        print("❌ ERROR saat drop tables:")
        print(e)

    finally:
        cur.close()
        conn.close()


# =========================
# CREATE SCHEMAS
# =========================
def create_schemas():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {DWH_SCHEMA};")
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {DM_SCHEMA};")

        conn.commit()
        print("Schemas created successfully.")

    except Exception as e:
        conn.rollback()
        print("❌ ERROR saat create schemas:")
        print(e)

    finally:
        cur.close()
        conn.close()


# =========================
# CREATE DWH TABLES
# =========================
def create_dwh_tables():
    conn = get_connection()
    cur = conn.cursor()

    try:
        # DIM CUSTOMER
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.{DIM_CUSTOMER} (
            customer_id INT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50)
        );
        """)

        # DIM PRODUCT
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.{DIM_PRODUCT} (
            product_id INT PRIMARY KEY,
            product_name VARCHAR(100),
            product_category VARCHAR(100)
        );
        """)

        # DIM STORE
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.{DIM_STORE} (
            store_id INT PRIMARY KEY,
            store_city VARCHAR(100)
        );
        """)

        # DIM DATE
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.{DIM_DATE} (
            sales_date TIMESTAMP PRIMARY KEY,
            year INT,
            month INT,
            day INT,
            hour INT
        );
        """)

        # FACT SALES (PARTITIONED TABLE)
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.{FACT_SALES} (
            sales_id INT,
            transaction_number VARCHAR(50),
            sales_date TIMESTAMP NOT NULL,
            store_id INT,
            customer_id INT,
            product_id INT,
            price NUMERIC(12,2),
            quantity INT,
            discount NUMERIC(5,2),
            sales NUMERIC(12,2),

            CONSTRAINT pk_fact_sales
                PRIMARY KEY (sales_id, sales_date),

            CONSTRAINT fk_customer
                FOREIGN KEY (customer_id)
                REFERENCES {DWH_SCHEMA}.{DIM_CUSTOMER}(customer_id),

            CONSTRAINT fk_product
                FOREIGN KEY (product_id)
                REFERENCES {DWH_SCHEMA}.{DIM_PRODUCT}(product_id),

            CONSTRAINT fk_store
                FOREIGN KEY (store_id)
                REFERENCES {DWH_SCHEMA}.{DIM_STORE}(store_id),

            CONSTRAINT fk_date
                FOREIGN KEY (sales_date)
                REFERENCES {DWH_SCHEMA}.{DIM_DATE}(sales_date)
        )
        PARTITION BY RANGE (sales_date);
        """)

        conn.commit()
        print("DWH tables created successfully.")

    except Exception as e:
        conn.rollback()
        print("❌ ERROR saat create DWH tables:")
        print(e)

    finally:
        cur.close()
        conn.close()


# =========================
# CREATE DAILY PARTITIONS
# =========================
def create_fact_sales_daily_partitions(start_date="2018-01-01", end_date="2018-05-10"):
    conn = get_connection()
    cur = conn.cursor()

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        current = start
        while current < end:
            next_day = current + timedelta(days=1)

            partition_name = f"{FACT_SALES}_{current.strftime('%Y%m%d')}"

            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.{partition_name}
            PARTITION OF {DWH_SCHEMA}.{FACT_SALES}
            FOR VALUES FROM ('{current.strftime('%Y-%m-%d')}')
                         TO ('{next_day.strftime('%Y-%m-%d')}');
            """)

            current = next_day

        conn.commit()
        print(f"Daily partitions created from {start_date} to {end_date}.")

    except Exception as e:
        conn.rollback()
        print("❌ ERROR saat create daily partitions:")
        print(e)

    finally:
        cur.close()
        conn.close()


# =========================
# CREATE DATAMART TABLES
# =========================
def create_datamart_tables():
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1️⃣ Total transaksi & user per jam
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DM_SCHEMA}.{DM_SUMMARY_SALES_PER_HOUR} (
            hour INT PRIMARY KEY,
            total_transactions INT,
            total_users INT
        );
        """)

        # 2️⃣ Total barang terjual per product
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DM_SCHEMA}.{DM_SUMMARY_PRODUCT_SALES} (
            product_id INT PRIMARY KEY,
            total_quantity_sold INT
        );
        """)

        # 3️⃣ Total barang terjual per store
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DM_SCHEMA}.{DM_SUMMARY_STORE_SALES} (
            store_id INT PRIMARY KEY,
            total_quantity_sold INT
        );
        """)

        # 4️⃣ Total penjualan harian
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DM_SCHEMA}.{DM_SUMMARY_DAILY_SALES} (
            sales_date DATE PRIMARY KEY,
            total_transactions INT,
            total_sales NUMERIC(12,2)
        );
        """)

        conn.commit()
        print("Datamart tables created successfully.")

    except Exception as e:
        conn.rollback()
        print("❌ ERROR saat create datamart tables:")
        print(e)

    finally:
        cur.close()
        conn.close()


# =========================
# RUN ALL DDL
# =========================
def run_ddl():
    create_schemas()
    create_dwh_tables()
    create_fact_sales_daily_partitions("2018-01-01", "2018-05-10")
    create_datamart_tables()
    print("=== DDL COMPLETED ===")


if __name__ == "__main__":
    run_ddl()