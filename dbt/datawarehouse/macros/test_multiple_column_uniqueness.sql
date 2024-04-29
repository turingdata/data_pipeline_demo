{% macro test_multiple_column_uniqueness(model, combination_of_columns) -%}

    {%- for column in combination_of_columns %}
            select
                '{{column}}' as column_name, {{column}} as column_value, count({{column}}) as value_counter
            from
                {{ model }}
            group by 1,2
            having count({{column}}) > 1

            {% if not loop.last -%}
            union all 
            {% endif %}

    {%- endfor -%}

{%- endmacro -%}