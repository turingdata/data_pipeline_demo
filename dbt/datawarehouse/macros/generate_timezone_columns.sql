-- get an UTC timestamp and break it in 3 columns, date-time, date, time for the UTC, CST and EST timezones.
--And if you want to add an alias for a new patern name just use the column_alias parameter to it
---------DO NOT ADD ALIAS AFTER CALLING THIS MACRO!
---------DO NOT ADD ALIAS AFTER CALLING THIS MACRO!
---------DO NOT ADD ALIAS AFTER CALLING THIS MACRO!
---------DO NOT ADD ALIAS AFTER CALLING THIS MACRO!
---------DO NOT ADD ALIAS AFTER CALLING THIS MACRO!
---------DO NOT ADD ALIAS AFTER CALLING THIS MACRO!
{% macro generate_timezone_columns(column_name, column_alias=column_name) %}  
    --init result generate_timezone_columns macro
    {{ column_name }} as {{ column_alias }}_datetime_utc
    , TRUNC({{ column_name }}) as {{ column_alias }}_date_utc
    , to_char({{ column_name }}, 'HH24:MI') as {{ column_alias }}_time_utc
    , convert_timezone('CST', {{ column_name }}) as {{ column_alias }}_datetime_cst
    , TRUNC(convert_timezone('CST', {{ column_name }})) as {{ column_alias }}_date_cst
    , to_char(convert_timezone('CST', {{ column_name }}), 'HH24:MI') as {{ column_alias }}_time_cst
    , convert_timezone('EST', {{ column_name }}) as {{ column_alias }}_datetime_est
    , TRUNC(convert_timezone('EST', {{ column_name }})) as {{ column_alias }}_date_est
    , to_char(convert_timezone('EST', {{ column_name }}), 'HH24:MI') as {{ column_alias }}_time_est
    --end result generate_timezone_columns macro
{% endmacro %}
