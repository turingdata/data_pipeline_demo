-- Convert amount fields from cents to dollars with 2 of precision
{% macro correcting_event_seq(column_name) %}  
    --init result correcting_event_seq macro
    CASE 
        WHEN trim({{ column_name }}) IS NULL OR trim({{ column_name }}) = '' THEN 0
        ELSE CAST(right(replace(trim({{ column_name }}), '', '0') ,19) AS bigint)
    END
    --end result correcting_event_seq macro
{% endmacro %}
