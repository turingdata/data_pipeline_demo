-- Convert amount fields from cents to dollars with 2 of precision
{% macro cents_to_dollars(column_name, precision=2) %}  
    --init result cents_to_dollars macro
    ( COALESCE(NULLIF(TRIM({{ column_name }}),'nan'), '0')::float / 100)::numeric(16, {{ precision }})
    --end result cents_to_dollars macro
{% endmacro %}
