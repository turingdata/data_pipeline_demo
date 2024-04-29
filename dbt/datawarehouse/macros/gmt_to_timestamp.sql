-- Convert datetime with GMT information into UTC format, checking some types of different inputs.


{% macro gmt_to_timestamp(column_name, else_column='event_date') %}
    --init result gmt_to_timestamp macro
    -- REDSHIFT does not accept sequece of miliseconds with over six number 9 and GMT
    -- This works '2022-04-08T15:18:47.999999731Z', '2022-04-08T15:18:47.123456789-04:00', '2022-04-08T15:18:47.999999-04:00'(sequence of six numbers nine only)
    -- This does not works '2022-04-08T15:18:47.999999731-04:00' (sequence with over six numbers nine and GMT)
    CASE 
        WHEN REGEXP_INSTR(
            {{ column_name }},
            '^([1][9][0-9]{2}|[2][0-9]{3})(-|\/)(0?[1-9]|[1][0-2])(-|\/)(0?[1-9]|[1-2][0-9]|3[0-1])($|((T| )([0-2][0-9]:[0-5][0-9]:[0-5][0-9])))($|Z$|.([0-9]{1,6}$|[0-9]{1,9}[\-|+][0-1][0-9]:[0-5][0-9]$|[0-9]{1,9}Z$))'
        )  > 0 THEN 
            CASE 
                WHEN REGEXP_INSTR({{ column_name }}, '[\-|+][0-9]{2}:[0-9]{2}$') > 0 
                    -- Get date and time with only 6 digits of miliseconds and concatenate with last 5 digits that are the GMT (-04:00)
                    THEN CAST(REGEXP_SUBSTR({{ column_name }}, '^([1][9][0-9]{2}|[2][0-9]{3})(-|\/)(0?[1-9]|[1][0-2])(-|\/)(0?[1-9]|[1-2][0-9]|3[0-1])($|((T| )([0-2][0-9]:[0-5][0-9]:[0-5][0-9])))($|.([0-9]{1,6}))') || REGEXP_SUBSTR({{ column_name }}, '[\-|+][0-9]{2}:[0-9]{2}$') AS TIMESTAMP WITH TIME ZONE) AT TIME ZONE 'UTC'
                ELSE
                    -- Does not contains GMT, so convert directly 
                    CAST(SUBSTRING({{ column_name }}, 1, 26) AS TIMESTAMP WITH TIME ZONE) AT TIME ZONE 'UTC'
            END
        ELSE CAST({{ else_column }} AS TIMESTAMP WITH TIME ZONE) AT TIME ZONE 'UTC'
    END
    --end result gmt_to_timestamp macro
{% endmacro %}
