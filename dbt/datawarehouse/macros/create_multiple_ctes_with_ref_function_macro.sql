{%- macro   create_multiple_ctes_with_ref_function_macro (list_of_table_info_tuples) -%}
    {%- for table_info in list_of_table_info_tuples -%} 

        {%- if table_info[2]== null -%}
            {{table_info[0]}} AS (
                select * from {{ ref(table_info[1]) }} 
            )
        {%- else %} 
            {{table_info[0]}} AS (   
                select 
                    {% for column_name_and_alias in table_info[2] -%} 
                        {%- if column_name_and_alias is string  -%}
                            {%- set column_name_and_alias = (column_name_and_alias, column_name_and_alias) -%}
                        {%- endif -%}

                        {%- if loop.first -%}
                            {{ column_name_and_alias[0] }} as {{ column_name_and_alias[1] }}
                        {%- endif %}

                        {%- if not loop.first %}
                            , {{ column_name_and_alias[0] }} as {{ column_name_and_alias[1] }}
                        {%- endif %}
                    {%- endfor %}
                from {{ ref(table_info[1]) }}
            )
        {%- endif -%}

        {%- if not loop.last %}
            ,
        {% endif %}

    {%- endfor -%}
{%- endmacro -%}