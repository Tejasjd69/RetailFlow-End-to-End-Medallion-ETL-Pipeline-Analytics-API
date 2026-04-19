# RetailFlow
### End-to-End Medallion ETL Pipeline & Analytics API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=flat-square&logo=pandas)

---

## Overview

RetailFlow is a production-grade data engineering system designed to process large-scale retail transaction datasets using the **Medallion Architecture**. The project demonstrates a full data lifecycle — from raw ingestion to a cleaned, validated state, and finally to a high-value, pre-aggregated analytics layer — exposed via a high-performance **FastAPI** backend.

---

## Core Highlights

- **Medallion Architecture** — Multi-tier Bronze → Silver → Gold pattern establishing a single source of truth for all business metrics
- **Robust ETL Pipeline** — Python & Pandas-based transformation with complex data cleaning and feature engineering
- **Data Quality Guardrails** — Custom assertion-based validation to prevent null leakage and ensure revenue calculation consistency
- **Optimized Query Performance** — Pre-aggregated Gold Layer in MySQL reduces API compute overhead compared to on-the-fly calculations

---

## Architecture

### Bronze Layer — Raw Ingestion
- Ingests raw retail transaction data in CSV format
- Preserves the original integrity of the source data with no transformations

### Silver Layer — Transformation & Cleaning
- **Schema Standardization** — Strips hidden whitespace and standardizes column names (`CustomerID`, `StockCode`, `InvoiceDate`)
- **Data Integrity** — Drops records with missing `CustomerID` to eliminate orphaned transactions
- **Business Logic** — Filters out non-revenue rows such as negative quantities and zero-price entries
- **Feature Engineering** — Derives `TotalAmount` (`Quantity × UnitPrice`) at the row level for downstream reporting

### Gold Layer — Curated Insights
- Aggregates Silver data into specialized analytical tables
- Computes key metrics: `TotalRevenue`, `TotalUnitsSold`, and `AvgPrice` per `StockCode`
- Stored in indexed MySQL tables purpose-built for low-latency API consumption

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend Framework | FastAPI (Async REST API) |
| Transformation Engine | Python & Pandas |
| Database | MySQL Server |
| ASGI Server | Uvicorn |

---

## Setup & Installation

**1. Configure the database**
```sql
CREATE DATABASE sales_pipeline;
```

**2. Install dependencies**
```bash
pip install pandas mysql-connector-python fastapi uvicorn
```

**3. Run the ETL pipeline**
```bash
python etl_pipeline.py
```

This processes data through all three layers and populates the MySQL database.

**4. Start the API server**
```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`

---

## API Reference

**GET** `/product_sales`  
Fetches pre-aggregated product performance data from the Gold Layer, including `TotalRevenue`, `TotalUnitsSold`, and `AvgPrice` per product.

**Interactive Docs**  
Swagger UI is available at `http://127.0.0.1:8000/docs`

---

## Project Structure

```
RetailFlow/
│
├── etl_pipeline.py        # Medallion ETL logic (Bronze -> Silver -> Gold)
├── main.py                # FastAPI app and route definitions
├── requirements.txt       # Python dependencies
├── data/
│   └── raw/               # Raw CSV input files
└── README.md
```

---

## License

This project is licensed under the MIT License.
