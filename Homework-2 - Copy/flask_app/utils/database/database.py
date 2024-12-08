import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime
import os

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path='flask_app/database/'):
        # Drop tables if purge is True
        if purge:
            tables_to_drop = ['skills', 'experiences', 'positions', 'institutions', 'feedback']
            for table in tables_to_drop:
                self.query(f"DROP TABLE IF EXISTS {table}")
            print("Tables dropped.")

        # Create tables in the correct dependency order
        sql_files = [
            'institutions.sql',
            'positions.sql',
            'experiences.sql',
            'skills.sql',
            'feedback.sql'
        ]
        for sql_file in sql_files:
            with open(os.path.join(data_path, 'create_tables', sql_file), 'r') as f:
                sql_commands = f.read()
                self.query(sql_commands)
        print("Tables created.")

        # Load and preprocess CSV data, replacing 'NULL' strings with None
        csv_files = [
            ('institutions.csv', 'institutions'),
            ('positions.csv', 'positions'),
            ('experiences.csv', 'experiences'),
            ('skills.csv', 'skills')
        ]

        for csv_file, table in csv_files:
            with open(os.path.join(data_path, 'initial_data', csv_file), mode='r') as file:
                reader = csv.reader(file)
                columns = next(reader)  # Read header for columns
                rows = [
                    [None if value == 'NULL' else value for value in row]  # Replace 'NULL' with None
                    for row in reader
                ]
                self.insertRows(table=table, columns=columns, parameters=rows)
        print("Data inserted in tables.")




    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        # Generate a string of placeholders (%s) for each column
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join(columns)
        
        # Create the SQL query dynamically based on table and columns
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        
        # Execute the query for each row in parameters
        for params in parameters:
            self.query(query, params)
        print(f"Rows inserted into {table}.")


    def getResumeData(self):
        data = {}

        # Fetch institutions
        institutions = self.query("SELECT * FROM institutions")
        print("Institutions:", institutions)  # Debugging output
        for institution in institutions:
            # Use 'inst_id' as defined in the institutions table
            institution_id = institution['inst_id']
            data[institution_id] = {
                'name': institution['name'],
                'city': institution['city'],
                'state': institution['state'],
                'positions': {}
            }

            # Fetch positions for this institution
            positions = self.query("SELECT * FROM positions WHERE inst_id = %s", (institution_id,))
            print(f"Positions for institution {institution_id}:", positions)  # Debugging output
            for position in positions:
                # Populate each position's data
                position_id = position['position_id']
                data[institution_id]['positions'][position_id] = {
                    'title': position['title'],
                    'start_date': position['start_date'],
                    'end_date': position['end_date'],
                    'responsibilities': position['responsibilities'],
                    'experiences': {}
                }

                # Fetch experiences for this position
                experiences = self.query("SELECT * FROM experiences WHERE position_id = %s", (position_id,))
                print(f"Experiences for position {position_id}:", experiences)  # Debugging output
                for experience in experiences:
                    experience_id = experience['experience_id']
                    data[institution_id]['positions'][position_id]['experiences'][experience_id] = {
                        'name': experience['name'],
                        'description': experience['description'],
                        'hyperlink': experience['hyperlink'],
                        'skills': {}
                    }

                    # Fetch skills for this experience
                    skills = self.query("SELECT * FROM skills WHERE experience_id = %s", (experience_id,))
                    print(f"Skills for experience {experience_id}:", skills)  # Debugging output
                    for skill in skills:
                        skill_id = skill['skill_id']
                        data[institution_id]['positions'][position_id]['experiences'][experience_id]['skills'][skill_id] = {
                            'name': skill['name'],
                            'skill_level': skill['skill_level']
                        }

        print("Final Resume Data:", data)  # Final output check
        return data