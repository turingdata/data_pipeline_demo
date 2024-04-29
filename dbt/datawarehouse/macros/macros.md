
{% docs create_multiple_ctes_with_ref_function_macro %}
This macro builds multiple CTEs from a list of tuples that contain cte alias, source table name, and optionally list of columns and aliases.
The first argument in each item in the given list becomes cte alias, the second one is used as the table reference. 
If provided third argument which should be a tuple of columns and their aliases.
Third element can be null, or list of column names, or list of column name and its alias.
If the macro argument doesn't contain the third item, the macro simply will give the statement of  'SELECT * FROM source table'.
If the possible third element of the tuple stores only column names and not aliases as a string, macro will treat the column name as its alias.
                  
### Usage:
{% raw %}
```
with 
{{ create_multiple_ctes_with_ref_function_macro ( 
    [ 
        ('cte_alias__dbt_model_1' , 'dbt_model_1', ['column_name1', ('column_name2','alias_column_name2') ] ),
        ('cte_alias__dbt_model_2' , 'dbt_model_2' ) 
    ]
}}
select 
    *
from cte_alias__dbt_model_1
join cte_alias__dbt_model_2 using(key_column)
```
{% endraw %}

## Returns:
Above code shown under usage, will be compiled as the equivalent of the code below;
```
with  
cte_alias__dbt_model_1 AS (   
    select 
        column_name1 as column_name1
        , column_name2 as alias_column_name2
    from "one_sample_dbt_model"
    )
,cte_alias__dbt_model_2 AS (
    select * from "another_sample_dbt_model" 
    )
select 
    * 
from cte_alias__dbt_model_1
join cte_alias__dbt_model_2 using(key_column)
```
{% enddocs %}


{% docs test_multiple_column_not_nullness %}
This macro will test whether multiple fields on a single dbt model are null or not. 
This macro test accepts two arguments, model and combination_of_columns, which are templated into the query. dbt will pass the values of model and 
column names accordingly.

When a new macro test is created,the name of the macro must be prefixed with a <test_> just before the main name of the macro. 
You can select as many columns as you want to test for nullness. 
These properties should be added inside < schema.yml > files in the same directory as the model. 
Do not include 'test_' prefix with the macros name in the .yml file.
When you run < dbt test> or < dbt run --select model >, dbt will tell you if each test in your project passes or fails. 

### Usage:


#### Update the schema.yml that includes the model names to be tested as below: 

```
models:
  - name: table_name_here
    tests:
      - multiple_column_not_nullness:
          combination_of_columns:
            - column_name_to_be_tested_1
            - column_name_to_be_tested_2

  - name: ...
```

### Usage Notes:
```
!!! <multiple_column_not_nullness> parameter name does not change     
!!! <combination_of_columns>  parameter name does not change 
!!! <column_name_to_be_tested_1>  value changes to the field name to be tested    
!!! <table_name_here>  value changes to the table/model name to be tested    
```

Execute command to test an individual model:
``` 
dbt test --select model_name_here 
```

## Returns:
Above code shown under usage, will be compiled as the equivalent of the code below;
```
select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
            select distinct
                'column_name_to_be_tested_1' as column_name, cast(column_name_to_be_tested_1 as varchar) as column_value
            from
                "database_name"."dbt_schema_name"."table_name_here"
            where column_name_to_be_tested_1 is null

            union all 
            
            select distinct
                'column_name_to_be_tested_2' as column_name, cast(column_name_to_be_tested_2 as varchar) as column_value
            from
                "database_name"."dbt_schema_name"."table_name_here"
            where column_name_to_be_tested_2 is null
) dbt_internal_test

```
{% enddocs %}




{% docs test_multiple_column_uniqueness %}
This macro will test whether multiple fields on a single dbt model are unique or not. 
This macro test accepts two arguments, model and combination_of_columns, which are templated into the query. dbt will pass the values of model and column names accordingly.

When a new macro test is created,the name of the macro must be prefixed with a <test_> just before the main name of the macro. 
You can select as many columns as you want to test for uniqueness. 
These properties should be added inside < schema.yml > files in the same directory as the model. 
Do not include 'test_' prefix with the macros name in the .yml file.
When you run < dbt test> or < dbt run --select model >, dbt will tell you if each test in your project passes or fails. 

### Usage:


#### Update the schema.yml that includes the model names to be tested as below: 

```
models:
  - name: table_name_here
    tests:
      - multiple_column_uniqueness:
          combination_of_columns:
            - column_name_to_be_tested_1
            - column_name_to_be_tested_2

  - name: ...
```

### Usage Notes:
```
!!! <multiple_column_uniqueness> parameter name does not change     
!!! <combination_of_columns>  parameter name does not change 
!!! <column_name_to_be_tested_1>  value changes to the field name to be tested    
!!! <table_name_here>  value changes to the table/model name to be tested    
```

Execute command to test an individual model:
``` 
dbt test --select model_name_here 
```

## Returns:
Above code shown under usage, will be compiled as the equivalent of the code below;
```
select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
            select
                'column_name_to_be_tested_1' as column_name, cast(column_name_to_be_tested_1 as VARCHAR) as column_value, 
                 count(column_name_to_be_tested_1) as value_counter
            from
                "database_name"."dbt_schema_name"."table_name_here"
            group by 1,2
            having count(column_name_to_be_tested_1) > 1

            union all 
            
            select
                'column_name_to_be_tested_2' as column_name, cast(column_name_to_be_tested_2 as varchar) as column_value,  
                 count(column_name_to_be_tested_2) as value_counter
            from
                "database_name"."dbt_schema_name"."table_name_here"
            group by 1 ,2
            having count(column_name_to_be_tested_2) > 1
) dbt_internal_test

```
{% enddocs %}



{% docs test_multiple_columns_to_exist %}

This macro will test whether multiple fields on a single dbt model exist or not. 
This macro accepts two arguments, model and combination_of_columns, which are templated into the query. dbt will pass the values of model and column names accordingly.

When a new macro test is created,the name of the macro must be prefixed with a <test_> just before the main name of the macro. 
You can select as many columns as you want to test for existence. This tests at the table level.
These properties should be added inside < schema.yml > files in the same directory as the model. 
Do not include 'test_' prefix with the macros name in the .yml file.
When you run < dbt test> or < dbt run --select model >, dbt will tell you if each test in your project passes or fails. 



### Usage:


#### Update the source.yml or schema.yml that includes the model names to be tested as below: 

```
models:
```
models:
  - name: table_name_here
    tests:
      - multiple_columns_to_exist:
          combination_of_columns:
            - column_name_to_be_tested_1
            - column_name_to_be_tested_2

  - name: ...
 
```

### Usage Notes:
```
!!! <multiple_columns_to_exist> parameter name does not change     
!!! <combination_of_columns>  parameter name does not change 
!!! <column_name_to_be_tested_1>  value changes to the field name to be tested    
!!! <table_name_here>  value changes to the table/model name to be tested    
```

Execute command to test an individual model:
``` 
dbt test --select model_name_here 
```

## Returns:

{% enddocs %}
