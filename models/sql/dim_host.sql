CREATE OR REPLACE TABLE dim_host AS
SELECT DISTINCT
    host_id,
    host_name,
    calculated_host_listings_count AS total_listings
FROM staging_listings;
