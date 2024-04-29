{{ 
    config(
        materialized = 'view'
        
    ) 
}}

WITH raw_table AS (
SELECT id,
    vehicle_id,
    trip_id,
    measurement_sequence,
    measurement_time,
    latitude,
    longitude,
    fuel_capacity,
    distance_traveled,
    fuel_remaining_percent,
    fuel_remaining_gallon,
    color
   FROM {{ ref( 'stg_trips' ) }}  
)
, where_condition As(
    SELECT trips.vehicle_id,
            trips.trip_id,
            max(trips.measurement_sequence) AS max
           FROM {{ ref( 'stg_trips' ) }} trips
          GROUP BY trips.vehicle_id, trips.trip_id
)
SELECT
     *
FROM  raw_table
WHERE 1=1
    AND (vehicle_id, trip_id, measurement_sequence) IN (SELECT * FROM where_condition)
