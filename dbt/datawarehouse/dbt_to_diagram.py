import yaml
import json
import argparse

class GenerateDiagram:
    # init method or constructor
    def __init__(self, path_yaml, path_json):
        self.path_yaml = path_yaml
        self.path_json = path_json
        self.tables = []
        self.references = []
        self.read_files()

    def read_files(self):
        f_yaml = open(self.path_yaml, "r") 
        self.schema = yaml.safe_load(f_yaml)

        f_json = open(self.path_json, "r")
        self.catalog = json.load(f_json)

    def generate_table_info(self):
        for table in self.catalog["nodes"]:
            temp_dict = {}
            if self.catalog["nodes"][table]["metadata"]["schema"] not in ['project_name_us_raw', 'project_name_us_staging', 'project_name_us_intermediary']:
                table_name = self.catalog["nodes"][table]["metadata"]["name"]
                schema_name = self.catalog["nodes"][table]["metadata"]["schema"]
                temp_dict['name'] = table_name
                temp_dict['schema'] = schema_name
                temp_dict['columns'] = self.handle_columns(self.catalog["nodes"][table]["columns"])
                self.tables.append(temp_dict)
                
    def handle_columns(self, column):
        col_temp_dict = {}
        for col in column:
            col_temp_dict[col] = {'type': self.replace_type(column[col]['type'])}
        return col_temp_dict

    def replace_type(self, strRep):
        dict_types = {
            "text" : "text",
            "date" : "date",
            "character varying" : "text",
            "timestamp without time zone" : "timestamp",
            "timestamp with time zone" : "timestamp",
            "integer" : "int",
            "bigint" : "int",
            "numeric" : "int",
            "double precision" : "float",
            "character varying(7)" : "text",
            "boolean" : "boolean",
            "text[]" : "text[]",
            "character varying[]" : "text[]",
            "shared_extensions.citext" : "text"
        }
        for word, replacement in dict_types.items():
            strRep = strRep.replace(word, replacement)
        return strRep

    def generate_ref_info(self):
        for table in self.tables:
            for column in table['columns']:
                for model in self.schema['models']:
                    if model['name'] == table['name']:
                        for col in model['columns']:
                            if col['name'] == column and 'tests' in col:
                                for tests in col['tests']:
                                    if 'relationships' in tests:
                                        to_table = tests['relationships']['to'].replace("ref('","").replace("')","")
                                        to_schema = next(item for item in self.tables if item['name'] == to_table)['schema']
                                        self.references.append({'from':f"{table['schema']}.{table['name']}.{col['name']}", 'to':f"{to_schema}.{to_table}.{tests['relationships']['field']}"})

    def save_dbdiagram(self, path):
        template_table = """
        Table {table_name} {{ 
        {columns}
        }}
        """
        template_ref = """
        Ref: {ref_from} > {ref_to}
        """
        self.generate_table_info()
        self.generate_ref_info()

        with open(path, 'w') as file:
            for table in self.tables:
                table_name = f"{table['schema']}.{table['name']}"
                col_aux = ''
                for column, type in table['columns'].items():
                    col_aux+=f"{column} {type['type']} \n"

                file.write(template_table.format(table_name=table_name, columns=col_aux))

            for ref in self.references:
                file.write(template_ref.format(ref_from=ref['from'], ref_to=ref['to']))

        print(f'File saved at "{path}"')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert DBT Config Files to DBDiagram input.')
    parser.add_argument('--models', help='Path to DBT models.yml', default=r'C:\Users\username\OneDrive\Documentos\project_name\projects\dbt\dw\datawarehouse\models\models.yml')
    parser.add_argument('--catalog', help='Path to DBT catalog.yml', default=r'C:\Users\username\OneDrive\Documentos\project_name\projects\dbt\dw\datawarehouse\target\catalog.json')
    parser.add_argument('--path', help='Path to save the dbdiagrams.txt with the output', default=r'C:\Users\username\Downloads\dbdiagram.txt')

    args = parser.parse_args()

    generate_diagram = GenerateDiagram(args.models, args.catalog)
    generate_diagram.save_dbdiagram(args.path)