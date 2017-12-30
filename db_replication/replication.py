import configparser
import pyodbc

import postgresql

import db_deploy.ddl_applying as ddl
import dbd_repr.dbd_to_ram as dbd2ram


class Replicator:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.schemas = dbd2ram.load(queries='../dbd_queries_mssql.cfg', db_config='../database.cfg')
        config = configparser.ConfigParser()
        config.read('../database.cfg', 'utf-8')

        self.mssql_server = config.get('SERVER', 'mssql_server')
        self.in_conn = pyodbc.connect(self.mssql_server)
        self.cursor = self.in_conn.cursor()

        self.postgres_server = config.get('SERVER', 'postgres_server')
        self.out_conn = postgresql.open(self.postgres_server)

    def __exit__(self):
        self.in_conn.close()
        self.out_conn.close()

    def create_empty_database(self):
        db = ddl.DbCreationConnection('../database.cfg', '../dbd_queries_mssql.cfg')
        db.deploy(db_name=self.db_name, schemas=self.schemas)
        self.out_conn.close()
        self.out_conn = postgresql.open(self.postgres_server + '/' + self.db_name.lower())

    def transfer_data(self):
        self.out_conn.execute('BEGIN TRANSACTION;')
        self.out_conn.execute('SET CONSTRAINTS ALL DEFERRED;')
        for schema in self.schemas:
            for table in schema.tables.values():
                self.cursor.execute(self.create_select_query(schema, table))
                batch = self.cursor.fetchmany(500)
                while len(batch) > 0:
                    # batch_query = 'BEGIN TRANSACTION;\n'
                    batch_query = ''
                    batch_query += ';\n'.join(
                        self.create_insert_query(schema, table, row)
                        for row
                        in batch
                    )
                    # batch_query += ';\nCOMMIT TRANSACTION;'
                    self.out_conn.execute(batch_query)
                    batch = self.cursor.fetchmany(500)
        self.out_conn.execute('COMMIT TRANSACTION;')

    def create_select_query(self, schema, table):
        query = 'SELECT ' + ', '.join(['[' + field + ']' for field in table.fields]) + ' '\
                'FROM [' + schema.name + '].[' + table.name + ']'
        return query

    def create_insert_query(self, schema, table, values):
        query = 'INSERT INTO ' + '"' + schema.name + '"."' + table.name + '" '\
                '(' + ', '.join(['"' + field + '"' for field in table.fields]) + ') '\
                'VALUES(' + ', '.join(
                                      ['\'' +
                                       str(value)
                                          .replace('\'', ' ')
                                       + '\''
                                       if value is not None
                                       else 'NULL'
                                       for value
                                       in values
                                      ]) + ')'
        return query
