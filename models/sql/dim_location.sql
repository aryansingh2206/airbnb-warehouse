CREATE OR REPLACE TABLE dim_location AS
SELECT
    row_number() OVER () AS location_id,
    LOWER(TRIM(CAST(neighbourhood_group AS VARCHAR))) AS neighbourhood_group,
    LOWER(TRIM(CAST(neighbourhood AS VARCHAR))) AS neighbourhood,
    AVG(latitude) AS latitude,
    AVG(longitude) AS longitude
FROM staging_listings
GROUP BY
    LOWER(TRIM(CAST(neighbourhood_group AS VARCHAR))),
    LOWER(TRIM(CAST(neighbourhood AS VARCHAR)));
