-- prepare a summary table
WITH COLUMNS AS (
    SELECT 
        table_schema AS schema_name,
        table_name,
        column_name,
        ordinal_position,
        is_nullable,
        udt_name AS data_type

    FROM  information_schema.columns
    WHERE table_schema='public'
)

, STATS AS (
    SELECT 
        schemaname AS schema_name,
        tablename AS table_name,
        attname AS column_name,
        null_frac AS null_value_fraction,
        n_distinct AS count_distinct_values,
        avg_width AS average_width

    FROM pg_catalog.pg_stats
    WHERE schemaname='public'
)

, ROW AS(
    SELECT 
        schemaname AS schema_name,
        RELNAME AS table_name,
        n_live_tup AS count_row

    FROM
    pg_catalog.pg_stat_user_tables 
    WHERE schemaname='public'
)

, FINAL AS(
    SELECT 
        COLUMNS.schema_name,
        COLUMNS.table_name,
        COLUMNS.column_name,
        COLUMNS.ordinal_position,
        COLUMNS.is_nullable,
        COLUMNS.data_type,
        ROW.count_row,
        STATS.null_value_fraction,
        STATS.count_distinct_values,
        STATS.average_width

    FROM COLUMNS 
    INNER JOIN STATS ON COLUMNS.table_name=STATS.table_name AND COLUMNS.column_name=STATS.column_name
    INNER JOIN ROW ON COLUMNS.table_name=ROW.table_name 

)

SELECT * FROM FINAL