import streamlit as st
import duckdb
import pandas as pd

st.title("Mini Airbnb Analytics Warehouse")

# -------------------------------------------
# LOAD RAW CSV FROM REPO
# -------------------------------------------

df_raw = pd.read_csv("data/raw/listings.csv")

# -------------------------------------------
# CLEAN DATA
# -------------------------------------------


def clean(df):
    df = df.copy()

    # Price cleaning
    if "price" in df.columns:
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace("$", "")
            .str.replace(",", "")
            .str.strip()
        )
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Convert numeric columns
    num_cols = [
        "minimum_nights", "number_of_reviews", "reviews_per_month",
        "availability_365", "number_of_reviews_ltm",
        "calculated_host_listings_count"
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Dates
    if "last_review" in df.columns:
        df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    return df

df_clean = clean(df_raw)



# -------------------------------------------
# CREATE IN-MEMORY DUCKDB WAREHOUSE
# -------------------------------------------


con = duckdb.connect(database=":memory:")

# Load staging
con.execute("CREATE TABLE staging_listings AS SELECT * FROM df_clean")

# DimLocation
con.execute("""
CREATE TABLE dim_location AS
SELECT
    row_number() OVER () AS location_id,
    LOWER(TRIM(CAST(neighbourhood AS VARCHAR))) AS neighbourhood,
    AVG(latitude) AS latitude,
    AVG(longitude) AS longitude
FROM staging_listings
GROUP BY LOWER(TRIM(CAST(neighbourhood AS VARCHAR)));
""")

# DimHost
con.execute("""
CREATE TABLE dim_host AS
SELECT DISTINCT
    host_id,
    host_name,
    calculated_host_listings_count AS total_listings
FROM staging_listings;
""")

# FactListing
con.execute("""
CREATE TABLE fact_listing AS
SELECT
    l.id AS listing_id,
    dl.location_id,
    h.host_id,
    l.name,
    l.room_type,
    l.price,
    l.minimum_nights,
    l.number_of_reviews,
    l.reviews_per_month,
    l.availability_365,
    l.number_of_reviews_ltm,
    l.last_review,
    l.license,
    l.latitude,
    l.longitude
FROM staging_listings l
LEFT JOIN dim_location dl
    ON LOWER(TRIM(CAST(l.neighbourhood AS VARCHAR))) = dl.neighbourhood
LEFT JOIN dim_host h
    ON l.host_id = h.host_id;
""")



# ---------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------
st.header(" Dataset Overview")

metrics = con.execute("""
SELECT 
    COUNT(*) AS total_listings,
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM fact_listing;
""").fetchdf().iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Listings", metrics["total_listings"])
col2.metric("Avg Price", f"${metrics['avg_price']:.2f}")
col3.metric("Min Price", f"${metrics['min_price']:.0f}")
col4.metric("Max Price", f"${metrics['max_price']:.0f}")

# ---------------------------------------------------
# Hotspot Areas
# ---------------------------------------------------
st.header(" Price Hotspots")

df_hotspot = con.execute("""
SELECT 
    ROUND(latitude, 3) AS lat_bucket,
    ROUND(longitude, 3) AS lon_bucket,
    COUNT(*) AS listings,
    AVG(price) AS avg_price
FROM fact_listing
GROUP BY lat_bucket, lon_bucket
ORDER BY avg_price DESC
LIMIT 25;
""").fetchdf()

st.dataframe(df_hotspot)

# ---------------------------------------------------
# Room Type Chart
# ---------------------------------------------------
st.header(" Avg Price by Room Type")

df_room = con.execute("""
SELECT room_type, AVG(price) AS avg_price
FROM fact_listing
GROUP BY room_type
ORDER BY avg_price DESC;
""").fetchdf()

st.bar_chart(df_room.set_index("room_type")["avg_price"])

# ---------------------------------------------------
# Price Distribution (Matplotlib)
# ---------------------------------------------------
import matplotlib.pyplot as plt

st.header(" Price Distribution")

df_dist = con.execute("SELECT price FROM fact_listing WHERE price IS NOT NULL;").fetchdf()

fig, ax = plt.subplots(figsize=(7, 3))
ax.hist(df_dist["price"], bins=50)
ax.set_xlabel("Price")
ax.set_ylabel("Count")
ax.set_title("Price Distribution")

st.pyplot(fig)
