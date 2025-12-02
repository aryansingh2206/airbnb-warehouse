CREATE OR REPLACE TABLE fact_listing AS
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
   AND LOWER(TRIM(CAST(l.neighbourhood_group AS VARCHAR))) = dl.neighbourhood_group
LEFT JOIN dim_host h
    ON l.host_id = h.host_id;
