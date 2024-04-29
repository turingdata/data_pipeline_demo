{% macro test_multiple_column_not_nullness(model, combination_of_columns) -%}

    {%- for column in combination_of_columns %}
        select distinct
            '{{column}}' as column_name, cast({{column}} as varchar) as column_value
        from
            {{ model }}
        where {{column}} is not null

        {% if not loop.last -%}
        union all 
        {% endif %}

    {%- endfor -%}

{%- endmacro -%}