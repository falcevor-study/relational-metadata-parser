""" Модуль, содержащий методы, позволяющие сгенерировать пустую базу PostgreSQL, получив на вход файл с
реляционным, либо текстовым предтсавлением метаданных.
"""
import configparser

import postgresql

from db_deploy.ddl_generator import DdlGenerator
from dbd_repr import dbd_to_ram
from ram_repr.ram_structure import Constraint
from ram_repr.ram_structure import Domain
from ram_repr.ram_structure import Index
from ram_repr.ram_structure import Schema
from ram_repr.ram_structure import Table
from xml_repr import xml_to_ram


class DbCreationConnection:
    """ Подключение к серверу БД, реализующее методы создания пустой базы.
    """
    def __init__(self, server_config, queries: str):
        self.queries = queries
        self.file = open(server_config, encoding='utf-8')
        self.config = configparser.ConfigParser()
        self.config.read_file(self.file)
        self.conn = postgresql.open(self.config.get('SERVER', 'postgres_server'))
        self.gen = DdlGenerator()

    def __exit__(self):
        self.conn.close()

    def begin_transaction(self):
        """ Стартовать транзакцию.

        :return: None
        """
        self.conn.execute('BEGIN TRANSACTION;')

    def commit(self):
        """ Зафиксировать транзакцию.

        :return: None
        """
        self.conn.execute('COMMIT;')

    def create_and_connect_database(self, db_name: str):
        """ Создать на сервере новую БД и сделать ее активной.

        :param db_name: название создаваемой БД
        :return: None`
        """
        self.conn.execute('DROP DATABASE IF EXISTS ' + db_name)
        self.conn.execute('CREATE DATABASE ' + db_name)
        self.conn.close()
        self.conn = postgresql.open(self.config.get('SERVER', 'postgres_server') + '/' + db_name.lower())

    def create_schema(self, schema: Schema):
        """ Создать в БД схему.

        :param schema: объект схемы.
        :return: None
        """
        ddl = self.gen.create_schema_dll(schema)
        self.conn.execute(ddl)

    def create_domain(self, domain: Domain, schema: Schema):
        """ Создать в БД домен.

        :param domain: объект домена.
        :param schema: объект схемы.
        :return: None
        """
        ddl = self.gen.create_domain_dll(domain, schema)
        self.conn.execute(ddl)

    def create_table(self, table: Table, schema: Schema):
        """ Создать таблицу в БД.

        :param table: объект таблицы.
        :param schema: объект схемы.
        :return: None
        """
        ddl = self.gen.create_table_ddl(table, schema)
        self.conn.execute(ddl)

    def create_constraint(self, constraint: Constraint, table: Table, schema: Schema):
        """ Создать ограничение в БД.

        :param constraint: объект индекса.
        :param table: объект таблицы.
        :param schema: объект схемы.
        :return: None
        """
        ddl = self.gen.create_constraint_ddl(constraint, table, schema)
        print(ddl)
        self.conn.execute(ddl)

    def create_index(self, index: Index, table: Table, schema: Schema):
        """ Создать индекс в БД.

        :param index: объект индекса.
        :param table: объект таблицы.
        :param schema: объект схемы.
        :return: None
        """
        ddl = self.gen.create_index_ddl(index, table, schema)
        self.conn.execute(ddl)

    def deploy(self, db_name: str, repr_file: str=None, schemas: list=None):
        """ Создать пустую базу данных PostgreSQL из реляционного, либо текстового представления метеданных.

        :param db_name: название создаваемой базы данных.
        :param repr_file: файл текстового, либо реляционного представления метеданных.
        :param server_config: файл с конфигурацией сервера PostgreSQL
        :return: None
        """
        if not schemas:
            if repr_file.endswith('.xml'):
                schemas = xml_to_ram.read(repr_file)
            elif repr_file.endswith('.db'):
                schemas = dbd_to_ram.load(queries=self.queries, db_file=repr_file)
            else:
                raise UnsupportedFileException()

            if schemas is None or len(schemas) == 0:
                raise UnsuccessfulTryException()

        self.create_and_connect_database(db_name)

        scripts = []
        scripts_foreign = []

        for schema in schemas:
            if len(schema.tables) == 0:
                continue
            scripts.append(self.gen.create_schema_dll(schema))
            for domain in schema.domains.values():
                scripts.append(self.gen.create_domain_dll(domain, schema))

            for table in schema.tables.values():
                scripts.append(self.gen.create_table_ddl(table, schema))

                for index in table.indexes:
                    scripts.append(self.gen.create_index_ddl(index, table, schema))

                for constraint in table.constraints:
                    if constraint.kind.upper() == 'FOREIGN':
                        scripts_foreign.append(self.gen.create_constraint_ddl(constraint, table, schema))
                    else:
                        scripts.append(self.gen.create_constraint_ddl(constraint, table, schema))

        deploy = 'BEGIN TRANSACTION;'
        deploy += '\n'.join(scripts)
        deploy += '\n'.join(scripts_foreign)
        deploy += 'COMMIT;'

        self.conn.execute(deploy)


class UnsupportedFileException(Exception):
    """ Подкласс исключений, порождаемых в следствие невозможности открытия файла
    с целью считывания из него представления метеданных.
    """
    def __str__(self):
        return 'Не удалось создать пустую БД. Неподдерживаемый файл.'


class UnsuccessfulTryException(Exception):
    """ Подкласс исключений, порождаемых в следсвтвие неуспешной попытки считвания
    метаданных из файла.
    """
    def __str__(self):
        return 'Не удалось создать пустую БД. Считывание схемы из файла закончилось неудачей.'
