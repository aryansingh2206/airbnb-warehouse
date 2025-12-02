import duckdb

con = duckdb.connect("warehouse.db")

# load staging data
con.execute("""
CREATE OR REPLACE TABLE staging_listings AS
SELECT * FROM read_parquet('data/staged/listings_clean.parquet');
""")

print("Loaded into DuckDB staging_listings")
