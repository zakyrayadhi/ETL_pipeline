from config import START_DATE, INITIAL_END_DATE, INITIAL_CSV_FILE, CSV_FILE
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

def run_initial_load():
    print("Starting Initial Load...")

    df_raw = extract_data()
    print("RAW:", df_raw.shape)
    print(df_raw.head())

    dim_customer = transform_dim_customer(df_raw)
    print("dim_customer:", dim_customer.shape)
    print(dim_customer.head())

    dim_product = transform_dim_product(df_raw)
    print("dim_product:", dim_product.shape)
    print(dim_product.head())

    dim_store = transform_dim_store(df_raw)
    print("dim_store:", dim_store.shape)
    print(dim_store.head())

    dim_date = transform_dim_date(df_raw)
    print("dim_date:", dim_date.shape)
    print(dim_date.head())

    fact_sales = transform_fact_sales(df_raw)
    print("fact_sales:", fact_sales.shape)
    print(fact_sales.head())

    load_dim_customer(dim_customer)
    load_dim_product(dim_product)
    load_dim_store(dim_store)
    load_dim_date(dim_date)
    load_fact_sales(fact_sales)

    print("Initial Load Completed!")
if __name__ == "__main__":
    run_initial_load()