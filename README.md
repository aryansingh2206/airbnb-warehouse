# 🏠 Mini Airbnb Analytics Warehouse

A lightweight but production-style data engineering project that ingests Airbnb listings, cleans and models them into a star-schema warehouse using DuckDB, and visualizes insights through a Streamlit dashboard. This project demonstrates modern analytical engineering concepts like ETL pipelines, dimensional modeling, exploratory analytics, and interactive visual dashboards.

---

## 🚀 Features

### 🔄 ETL Pipeline
- Ingest raw Airbnb dataset (`listings.csv`)
- Clean & normalize key fields (price, dates, numerics)
- Store cleaned data as Parquet in `data/staged/`

### 🗄️ Data Warehouse (DuckDB)
Dimensional star schema:
- **fact_listing**
- **dim_location**
- **dim_host**
- **staging_listings**

Built using simple SQL models via `scripts/run_models.py`.

### 📊 Interactive Dashboard (Streamlit)
- Summary metrics (total listings, price stats)
- Top neighborhoods / hotspot areas
- Average price by room type
- Price distribution histogram
- Geo-bucketed pricing hotspots (works for all cities)

---

## 📁 Project Structure

```

airbnb-warehouse/
│
├── data/
│   ├── raw/              # raw input CSVs
│   ├── staged/           # cleaned Parquet files
│   └── outputs/
│
├── scripts/
│   ├── clean_listing.py  # data cleaning
│   ├── load_to_duckdb.py # load staged data
│   └── run_models.py     # build DuckDB models
│
├── models/
│   └── sql/
│       ├── dim_location.sql
│       ├── dim_host.sql
│       └── fact_listing.sql
│
├── dashboards/
│   └── app.py            # Streamlit dashboard
│
├── warehouse.db          # DuckDB warehouse (ignored by git)
├── requirements.txt
└── README.md

````

---

## 🔧 Setup Instructions

### 1️⃣ Create & activate virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
````

### 2️⃣ Add the Airbnb dataset

Place your `listings.csv` in:

```
data/raw/listings.csv
```

### 3️⃣ Run ETL

```bash
python scripts/clean_listing.py
python scripts/load_to_duckdb.py
python scripts/run_models.py
```

### 4️⃣ Launch dashboard

```bash
streamlit run dashboards/app.py
```

---

## 📈 Example Insights

* Price hotspots based on geo-buckets
* Room type pricing comparison
* Distribution of nightly rates
* Neighborhood-level patterns (if available)

---

