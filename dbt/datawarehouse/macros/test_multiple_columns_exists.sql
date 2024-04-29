{% macro test_multiple_columns_to_exist(model, combination_of_columns) -%}

    select 
        {%- for column in combination_of_columns %}
            {{column}}
            {% if not loop.last -%}
            ,

            {% endif %}

        {%- endfor -%}
        
    from {{ model }}

    where false


{%- endmacro -%}
