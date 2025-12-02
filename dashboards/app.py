import streamlit as st
import duckdb

# Connect in read-only mode to prevent file locking
con = duckdb.connect("warehouse.db", read_only=True)

st.title("Mini Airbnb Analytics Warehouse")
st.write("Analytics automatically adapted to your city's dataset 🚀")

# -------------------------------------------
# 1. Show high-level metrics
# -------------------------------------------
st.header("📊 Quick Overview")

metrics = con.execute("""
SELECT 
    COUNT(*) AS total_listings,
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM fact_listing;
""").fetchdf().iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Listings", f"{metrics['total_listings']}")
col2.metric("Avg Price", f"${metrics['avg_price']:.2f}")
col3.metric("Min Price", f"${metrics['min_price']:.0f}")
col4.metric("Max Price", f"${metrics['max_price']:.0f}")

# -------------------------------------------
# 2. Neighborhood-level pricing (fallback for cities with valid names)
# -------------------------------------------
st.header("🏘️ Top Neighborhoods by Avg Price")

df_neigh = con.execute("""
SELECT d.neighbourhood,
       COUNT(*) AS listings,
       AVG(f.price) AS avg_price
FROM fact_listing f
JOIN dim_location d ON f.location_id = d.location_id
WHERE d.neighbourhood IS NOT NULL AND d.neighbourhood <> 'none'
GROUP BY d.neighbourhood
ORDER BY avg_price DESC
LIMIT 20;
""").df()

if df_neigh.empty:
    st.info("This dataset has no usable neighbourhood names. Showing hotspot areas instead ↓")
else:
    st.dataframe(df_neigh)

# -------------------------------------------
# 3. Hotspot Areas (always works)
# -------------------------------------------
st.header("🔥 Price Hotspots (lat/lon buckets)")

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
""").df()

st.dataframe(df_hotspot)

# -------------------------------------------
# 4. Room type comparison
# -------------------------------------------
st.header("🛏️ Avg Price by Room Type")

df_room = con.execute("""
SELECT room_type, COUNT(*) AS listings, AVG(price) AS avg_price
FROM fact_listing
GROUP BY room_type
ORDER BY avg_price DESC;
""").df()

st.bar_chart(df_room.set_index("room_type")["avg_price"])

# -------------------------------------------
# 5. Price distribution
# -------------------------------------------
st.header("📈 Price Distribution")

df_dist = con.execute("SELECT price FROM fact_listing;").df()
st.caption("Showing price histogram for all listings")

# -------------------------------------------
# 5. Price Distribution (Matplotlib)
# -------------------------------------------
import matplotlib.pyplot as plt

st.header("📈 Price Distribution")

df_dist = con.execute("SELECT price FROM fact_listing WHERE price IS NOT NULL;").df()

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df_dist["price"], bins=50)
ax.set_title("Price Distribution")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Count")

st.pyplot(fig)

