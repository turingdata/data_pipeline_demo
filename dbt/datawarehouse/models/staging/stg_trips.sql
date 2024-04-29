{{ 
    config(
        materialized = 'table',
        unique_key = 'id',
        on_schema_change='sync_all_columns',
        
    ) 
}}
-- post_hook = """delete from {{this}} where dbt_execution < CAST('{{ run_started_at.strftime('%Y-%m-%d %H:%M:%S.%f') }}' as timestamp)"""

WITH raw_table AS (
    SELECT
    	id
        , vehicle_id
        , trip_id
        , measurement_sequence
        , measurement_time
        , latitude
        , longitude
        , fuel_capacity
        , distance_traveled
        , fuel_remaining_percent
        , fuel_remaining_gallon
        , color
        , loaded_at AS loaded_at_to_landing_zone
        , CAST('{{ run_started_at.strftime("%Y-%m-%d %H:%M:%S.%f") }}' AS TIMESTAMP) AS dbt_execution
    FROM
        {{ source( 'src_oltp', 'raw_trips' ) }}
)
SELECT
     *
FROM  raw_table
WHERE
    1 = 1

