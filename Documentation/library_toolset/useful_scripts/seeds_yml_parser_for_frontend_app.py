#%%
import os
from re import A
import sys
current_directory = os.getcwd()
home_directory = current_directory+'/..'
sys.path.append(home_directory)
from distutils.command.config import config
import sqlalchemy
import csv
import pandas as pd
import numpy as np
import ast
from ast import *
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

#%%
#Establish and test the database connection
from modules.database_tools import connect_database
engine_ = connect_database(connection_name='frontend-dev')
schema='public'

#Test Connection
query_test_connection="SELECT 'Connection is Successfull' AS Connection_Status, NOW() AS TIMESTAMP "
pd.read_sql_query(sql=query_test_connection,con=engine_)

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

#%%
#Write the summary table to the DB
from modules.database_tools import connect_database
engine_local = connect_database(connection_name='cabak')
schema='public'

#Test Connection
query_test_connection="SELECT 'Connection is Successfull' AS Connection_Status, NOW() AS TIMESTAMP "
pd.read_sql_query(sql=query_test_connection,con=engine_local)

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
# %%
#Write a df to a table
df = pd.read_csv('../data/outputs/frontend_publicschema_tables/01_frontend_publicschema_stats.csv', index_col=0)
df

# df.to_sql(name='summary__schema', if_exists='fail', con=engine_local)

########################
# %%

#Parse seed yml files
import pandas as pd
from yaml import safe_load
import json
from pandas import json_normalize

with open('../data/inputs/seeds.yml', 'r') as yml_file:
    yml_file = safe_load(yml_file)

with open('../data/outputs/seeds.json', 'w') as json_file:
    json.dump(yml_file, json_file)

df_yml = pd.read_json('../data/outputs/seeds.json').T.reset_index()
df_yml.columns = ['table_name', 'execution_plan', 'source_filename', 'overrides']
df_yml
#%%
json_normalized = json_normalize(yml_file)
json_normalized

#%%
#Filter rows without a source file
df_yml_1 = df_yml.loc[df_yml['source_filename'].isnull()==False].copy()

#parse the execution column for column info
df_yml_1['column_names']=[i['source_columns'] for i in df_yml_1['execution_plan']]

#parse the relationships
df_yml_1['relationships'] =[i['relationships'] if i.get('relationships') else '' for i in df_yml_1['execution_plan'] ]
df_yml_1

#Convert the df to long version over columns
df_yml_2 = df_yml_1.explode('column_names')

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------


#extract the column names
values = []
for i in df_yml_2.column_names:
    try:
        value= i['column_name']
    except:
        value= ''
    values.append(value)

df_yml_2['column_name'] =values




#extract the attribute names
values = []
for i in df_yml_2.column_names:
    try:
        value= i['destination']['attribute_mapping']
    except:
        value= ''
    values.append(value)

df_yml_2['column_name_mapped_from'] =values


#extract the transformation names
values = []
for i in df_yml_2.column_names:
    try:
        value= i['destination']['transform']
    except:
        value= ''
    values.append(value)

df_yml_2['transformation'] =values


df_yml_2
########################
# %%

#extract the relationship info

values = []
for i in df_yml_2.relationships:
    try:
        value= i[0]['related_to']
    except:
        value= ''
    values.append(value)

df_yml_2['table_related_to'] =values


values = []
for i in df_yml_2.relationships:
    try:
        value= i[0]['lookup_key']
    except:
        value= ''
    values.append(value)

df_yml_2['table_lookup_key'] =values


values = []
for i in df_yml_2.relationships:
    try:
        value= i[0]['foreign_key']
    except:
        value= ''
    values.append(value)

df_yml_2['table_foreign_key'] =values


values = []
for i in df_yml_2.relationships:
    try:
        value= i[0]['destination']['attribute_mapping']
    except:
        value= ''
    values.append(value)

df_yml_2['table_destination_attribute_mapping'] =values

#%%
df_yml_3 = df_yml_2.copy().reset_index().astype('str')
df_yml_3
# %%
df_yml_4 = df_yml_3[['table_name','column_name','source_filename', 'relationships',  'column_name_mapped_from',
       'transformation', 'table_related_to', 'table_lookup_key',
       'table_foreign_key', 'table_destination_attribute_mapping']].copy()
#Reorganize the columns
df_yml_4.to_csv('../data/outputs/frontend_publicschema_tables/02_frontend_schema_mapping.csv', index=False)
# %%

#write the file to DB
df_yml_4.to_sql(name='mapping_phoenix_tirs_frontend', if_exists='fail', con=engine_local)

# %%
df_yml_4
# %%
df_merged = df.merge(df_yml_4, how='left', left_on=['column_name'], right_on=['column_name']).sort_values('table_lookup_key')
# %%
