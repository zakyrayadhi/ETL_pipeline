# Grocery Sales Data Warehouse ETL Pipeline

## 📌 Project Overview

This project implements an end-to-end **ETL (Extract, Transform, Load) pipeline** to build a structured **Data Warehouse** from grocery sales transaction data.

The pipeline extracts raw transactional data, performs transformation using Python, and loads the processed data into a PostgreSQL Data Warehouse using a **Star Schema architecture**.

This project evaluates two different data loading strategies:

1. **Full Reload**

   * The complete dataset is loaded and processed from the beginning.
   * The pipeline reads directly from `grocery_sales.csv`.
   * This approach simulates a scenario where all available data is reprocessed every time.

2. **Incremental Load**

   * The dataset is divided into historical data and newly arriving data.
   * The initial load populates the Data Warehouse with historical records.
   * The delta load processes only newly added records.
   * This approach simulates a production-like incremental data ingestion workflow.

The objective is to compare both approaches and measure the efficiency improvement achieved through incremental loading.

---

# 🎯 Objectives

* Build a Data Warehouse using Star Schema modeling
* Develop an ETL pipeline using Python
* Transform raw transactional data into analytical structures
* Implement dimension and fact table relationships
* Implement full reload and incremental loading strategies
* Compare ETL execution performance between loading approaches

---

# 🏗️ ETL Architecture

The pipeline follows an ETL workflow:

![ETL Workflow](docs/etl_flow.png)

High-level workflow:

```
Source Data
     |
     v
 Extract
     |
     v
 Transform
     |
     v
 Load
     |
     v
PostgreSQL Data Warehouse
```

---

# 🛠️ Tech Stack

| Category                | Technology       |
| ----------------------- | ---------------- |
| Programming Language    | Python           |
| Database                | PostgreSQL       |
| Data Processing         | Pandas           |
| Database Connector      | Psycopg2         |
| SQL Client              | DBeaver          |
| Data Modeling           | Star Schema      |
| Development Environment | Jupyter Notebook |
| Version Control         | Git & GitHub     |

---

# 📂 Project Structure

```
grocery-sales-datawarehouse/

├── data/
│   ├── grocery_sales.csv
│   ├── initial_load_data.csv
│   └── delta_load_data.csv
│
├── docs/
│   ├── etl_flow.png
│   └── star_schema.png
│
├── notebooks/
│   ├── full_reload.ipynb
│   ├── initial_load_analysis.ipynb
│   └── delta_load_analysis.ipynb
│
├── scripts/
│   ├── ddl.py
│   ├── initial_load.py
│   ├── delta_load.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── requirements.txt
└── README.md
```

---

# 🗄️ Data Warehouse Design

The Data Warehouse follows a **Star Schema architecture**.

![Star Schema](docs/star_schema.png)

The schema consists of:

* Dimension tables containing descriptive information
* Fact table containing transactional measurements

---

# ⭐ Dimension Tables

## dim_customer

Stores customer information.

| Column      | Description                |
| ----------- | -------------------------- |
| customer_id | Unique customer identifier |
| first_name  | Customer first name        |
| last_name   | Customer last name         |

---

## dim_product

Stores product information.

| Column       | Description               |
| ------------ | ------------------------- |
| product_id   | Unique product identifier |
| product_name | Product name              |
| category     | Product category          |

---

## dim_store

Stores store information.

| Column     | Description             |
| ---------- | ----------------------- |
| store_id   | Unique store identifier |
| store_city | Store city location     |

---

## dim_date

Stores date and time information.

| Column  | Description       |
| ------- | ----------------- |
| date_id | Date identifier   |
| date    | Transaction date  |
| year    | Transaction year  |
| month   | Transaction month |
| day     | Transaction day   |
| hour    | Transaction hour  |

---

# 📊 Fact Table

## fact_sales

Stores transactional sales information.

| Column             | Description            |
| ------------------ | ---------------------- |
| sales_id           | Transaction identifier |
| transaction_number | Transaction number     |
| sales_date         | Transaction timestamp  |
| customer_id        | Customer foreign key   |
| product_id         | Product foreign key    |
| store_id           | Store foreign key      |
| date_id            | Date foreign key       |
| price              | Product price          |
| quantity           | Quantity purchased     |
| discount           | Applied discount       |
| sales              | Total sales amount     |

---

# 🔄 ETL Pipeline

## 1. Extract

The extraction process reads transaction data from CSV files.

The project implements two loading scenarios.

---

## Full Reload Scenario

Source:

```
grocery_sales.csv
```

The full reload scenario processes the entire dataset.

Workflow:

```
grocery_sales.csv
        |
        v
 Extract All Records
        |
        v
 Transform
        |
        v
 Load
        |
        v
Data Warehouse
```

Characteristics:

* Processes all available records
* Simple implementation
* Suitable for smaller datasets
* Execution time increases as data volume grows

---

## Incremental Load Scenario

The dataset is split into:

| Dataset               | Purpose                                           |
| --------------------- | ------------------------------------------------- |
| initial_load_data.csv | Historical records for first warehouse population |
| delta_load_data.csv   | New incoming records for incremental updates      |

Workflow:

```
initial_load_data.csv
          |
          v
    Initial Load
          |
          v
Data Warehouse


delta_load_data.csv
          |
          v
     Delta Load
          |
          v
Append New Records
```

The delta load process only processes new transactions after the initial warehouse population.

---

# 2. Transform

The transformation process prepares raw data into analytical structures.

Transformation steps:

* Data cleaning
* Data type conversion
* Creating dimension tables
* Creating date dimension
* Creating fact table
* Maintaining relationships between tables

---

# 3. Load

The loading process inserts transformed data into PostgreSQL.

Loading order:

```
Dimension Tables
        |
        v
   Fact Table
```

Dimension tables are loaded first to maintain foreign key relationships before inserting transactional records.

---

# 📓 Notebook Workflow

The ETL process is executed using three Jupyter Notebooks.

## 1. Full Reload Notebook

Notebook:

```
full_reload.ipynb
```

Purpose:

* Load complete data from `grocery_sales.csv`
* Process all available records
* Simulate full warehouse refresh

---

## 2. Initial Load Notebook

Notebook:

```
initial_load.ipynb
```

Purpose:

* Load historical data from `initial_load_data.csv`
* Prepare initial Data Warehouse state before incremental updates

Note:
The initial load execution time is not included in the performance comparison because it represents warehouse initialization.

---

## 3. Delta Load Notebook

Notebook:

```
delta_load.ipynb
```

Purpose:

* Process new records from `delta_load_data.csv`
* Append only new transactions
* Simulate continuous incremental ingestion

---

# 🚀 ETL Performance Comparison

The pipeline performance was evaluated between full reload and delta load scenarios.

| Loading Method | Dataset             | Execution Time |
| -------------- | ------------------- | -------------: |
| Full Reload    | grocery_sales.csv   |  15.91 seconds |
| Delta Load     | delta_load_data.csv |   1.17 seconds |

Performance improvement:

* **13.6x faster execution**
* **92.6% reduction in processing time**

The result demonstrates that incremental loading significantly improves ETL efficiency by avoiding unnecessary processing of existing records.

---

# ✅ Data Validation

Validation checks performed:

* Verify loaded record counts
* Validate dimension and fact table relationships
* Ensure primary key uniqueness
* Check foreign key consistency

---

# ▶️ How to Run

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Configure Database Connection

Update database credentials in:

```
config.py
```

---

## 3. Execute Notebooks

### Full Reload

```
notebooks/full_reload.ipynb
```

### Initial Load

```
notebooks/initial_load.ipynb
```

### Delta Load

```
notebooks/delta_load.ipynb
```

---

# 🚀 Future Improvements

* Implement Apache Airflow for ETL scheduling and workflow orchestration
* Add automated data quality monitoring
* Add ETL logging and execution tracking
* Containerize pipeline using Docker
* Deploy Data Warehouse infrastructure on cloud platforms

---

# 👤 Author

**Zaky Rayadhi**

Data Analyst | Python | SQL | Data Warehouse

GitHub: https://github.com/zakyrayadhi
