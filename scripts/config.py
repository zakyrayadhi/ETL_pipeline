# postgresql connection
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "grocery_dw"
DB_USER = "postgres"
DB_PASSWORD = "admin"

# schema config
DWH_SCHEMA = "dwh"
DM_SCHEMA = "datamart"

# lokasi file
INITIAL_CSV_FILE = "data/initial_load.csv"
DELTA_CSV_FILE = "data/delta_load.csv"

# Periode Initial Load
START_DATE = "2018-01-01"
INITIAL_END_DATE = "2018-05-09"

# Selected City
CITIES = [
    "Depok",
    "Bogor",
    "Jakarta",
    "Denpasar",
    "Bandung",
    "Tangerang",
]

# Nama Tabel
STAGING_TABLE = "grocery_sales_raw"
DIM_CUSTOMER = "dim_customer"
DIM_PRODUCT = "dim_product"
DIM_STORE = "dim_store"
DIM_DATE = "dim_date"
FACT_SALES = "fact_sales"

# datamart tables
DM_SUMMARY_SALES_PER_HOUR = "summary_sales_per_hour"
DM_SUMMARY_PRODUCT_SALES = "summary_product_sales"
DM_SUMMARY_STORE_SALES = "summary_store_sales"
DM_SUMMARY_DAILY_SALES = "summary_daily_sales"
