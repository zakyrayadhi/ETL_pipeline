import pandas as pd

def transform_dim_customer(df):
    dim_customer = df[['customer_id', 'first_name', 'last_name']].drop_duplicates()
    return dim_customer

def transform_dim_product(df):
    dim_product = df[['product_id', 'product_name', 'category_name']].drop_duplicates()
    dim_product = dim_product.rename(columns={'category_name': 'product_category'})
    return dim_product

def transform_dim_store(df):
    dim_store = df[['store_id', 'store_city']].drop_duplicates()
    return dim_store

def transform_dim_date(df):
    df = df.copy()
    df['sales_date'] = pd.to_datetime(df['sales_date'], format='mixed')

    dim_date = df[['sales_date']].drop_duplicates().copy()
    dim_date['year'] = dim_date['sales_date'].dt.year
    dim_date['month'] = dim_date['sales_date'].dt.month
    dim_date['day'] = dim_date['sales_date'].dt.day
    dim_date['hour'] = dim_date['sales_date'].dt.hour

    # hanya pilih kolom yang ada di tabel DWH
    dim_date = dim_date[['sales_date', 'year', 'month', 'day', 'hour']]
    return dim_date

def transform_fact_sales(df):
    df = df.copy()
    df['sales_date'] = pd.to_datetime(df['sales_date'], format='mixed')

    fact_sales = df[[
        'sales_id',
        'transaction_number',
        'sales_date',
        'store_id',
        'customer_id',
        'product_id',
        'quantity',
        'price',
        'discount',
        'sales'
    ]].copy()

    return fact_sales