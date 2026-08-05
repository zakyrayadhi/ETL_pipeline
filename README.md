# Grocery Sales Data Warehouse ETL Pipeline

## 📌 Project Overview

This project implements an end-to-end **ETL (Extract, Transform, Load) pipeline** to build a structured **Data Warehouse** from grocery sales transaction data.

The pipeline extracts raw transactional data, performs data transformation using Python, and loads the processed data into a PostgreSQL Data Warehouse using a **Star Schema architecture**.

This project evaluates two different data loading strategies:

1. **Full Reload**

   * Reloads the complete dataset from the beginning every time the pipeline runs.
   * Simulates a scenario where all available data is always processed.

2. **Incremental Load (Initial Load + Delta Load)**

   * Splits data into historical records and newly arriving records.
   * Initial load populates the Data Warehouse with existing historical data.
   * Delta load processes only new incoming records.
   * Simulates a production-like incremental data ingestion workflow.

The objective is to compare both approaches and measure the efficiency improvement achieved through incremental loading.

---

# 🎯 Objectives

* Build a Data Warehouse using Star Schema modeling
* Develop an ETL pipeline using Python
* Transform raw transactional data into analytical structures
* Implement dimension and fact table relationships
* Implement full reload and incremental loading strategies
* Compare ETL performance between different loading approaches

---

# 🏗️ ETL Architecture

The pipeline follows a standard ETL workflow:

![ETL Workflow](docs/etl_flow.png)

Workflow:

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

| Category             | Technology   |
| -------------------- | ------------ |
| Programming Language | Python       |
| Database             | PostgreSQL   |
| Data Processing      | Pandas       |
| Database Connector   | Psycopg2     |
| SQL Client           | DBeaver      |
| Data Modeling        | Star Schema  |
| Version Control      | Git & GitHub |

---

# 📂 Project Structure

```
grocery-sales-datawarehouse/
│
├── data/
│   ├── grocery_sales.csv
│   ├── initial_load_data.csv
│   └── delta_load_data.csv
│
├── docs/
│   ├── etl_flow.png
│   └── star_schema.png
│
├── config.py
├── extract.py
├── transform.py
├── load.py
│
├── ddl.py
├── full_reload.py
├── initial_load.py
├── delta_load.py
│
├── requirements.txt
└── README.md
```

---

# 🗄️ Data Warehouse Design

The Data Warehouse follows a **Star Schema architecture**.

![Star Schema](docs/star_schema.png)

The schema consists of:

* Dimension tables containing descriptive attributes
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

Stores date and time information for transaction analysis.

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
| quantity           | Quantity purchased     |
| price              | Product price          |
| discount           | Applied discount       |
| sales              | Total sales amount     |

---

# 🔄 ETL Pipeline

## 1. Extract

The extraction process reads transaction data from CSV files.

The project implements two loading scenarios:

### Full Reload Dataset

Source:

```
grocery_sales.csv
```

Purpose:

* Process all available transaction records
* Simulate complete warehouse refresh

---

### Incremental Load Dataset

The source dataset is divided into:

| Dataset               | Purpose                                                |
| --------------------- | ------------------------------------------------------ |
| initial_load_data.csv | Historical records used for first warehouse population |
| delta_load_data.csv   | New incoming transactions for incremental updates      |

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

Dimension tables are loaded first to ensure foreign key relationships are available before inserting transactional records.

---

# ⚡ Loading Strategy

## Full Reload

The full reload approach processes the entire dataset every time.

Workflow:

```
grocery_sales.csv
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
Data Warehouse
```

Advantages:

* Simple implementation
* Easy to maintain

Limitations:

* Processing time increases as data grows
* Existing records are processed repeatedly

---

## Incremental Load

The incremental loading approach simulates real-world data ingestion.

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

The delta load process identifies new transactions based on the latest transaction timestamp stored in the Data Warehouse.

Advantages:

* Processes only new records
* Reduces execution time
* More scalable for continuous data updates

---

# 🚀 ETL Performance Comparison

The pipeline performance was tested using both loading strategies.

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

## 1. Clone Repository

```bash
git clone <repository-url>
cd grocery-sales-datawarehouse
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Database Connection

Update database credentials in:

```
config.py
```

Example:

```python
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "warehouse"
DB_USER = "postgres"
DB_PASSWORD = "password"
```

---

## 4. Create Database Tables

```bash
python ddl.py
```

---

## 5. Run Full Reload

```bash
python full_reload.py
```

---

## 6. Run Initial Load

```bash
python initial_load.py
```

---

## 7. Run Delta Load

```bash
python delta_load.py
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

GitHub: <your-github-link>
