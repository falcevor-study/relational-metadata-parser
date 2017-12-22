import configparser
import errno
import os
import sqlite3
import uuid

from dbd_repr.dbd_structure import BEGIN_TRANSACTION
from dbd_repr.dbd_structure import COMMIT
from dbd_repr.dbd_structure import SQL_DBD_Init
from dbd_repr.dbd_temp_structure import SQL_TMP_INIT
from ram_repr.ram_structure import Constraint
from ram_repr.ram_structure import ConstraintDetail
from ram_repr.ram_structure import Domain
from ram_repr.ram_structure import Field
from ram_repr.ram_structure import Index
from ram_repr.ram_structure import IndexDetail
from ram_repr.ram_structure import Schema
from ram_repr.ram_structure import Table


class DbdUploadConnection:
    """ Класс, реализующий подключение к базе SQLite лдя создания DBD-представления схемы БД.
    """
    def __init__(self, config_file: str, db_file: str):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, 'utf-8')
        self._drop_if_exists(db_file)
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.conn.close()

    @staticmethod
    def _drop_if_exists(file_name: str):
        """ Удалить файл, если он существует.

        :param file_name: Путь к удаляемому файлу.
        :return: None
        """
        try:
            os.remove(file_name)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def create_dbd_repr(self):
        """ Создать основные источники для струтктурных элементов.

        :return: None
        """
        self.cursor.executescript(SQL_DBD_Init)

    def create_tmp_dbd_repr(self):
        """ Создать временные источники для структурных элементов.

        :return: None
        """
        self.cursor.executescript(SQL_TMP_INIT)

    def fill_main_tables(self):
        """ Запустить скрипт переливки данных из временных источников в основные.

        :return: None
        """
        self.cursor.executescript(self.config.get('PROCESSING', 'fill_main_tables'))

    def upload_schema(self, schema: Schema):
        """ Выгрузить данные из объекта схемы во временных источник схем.

        :param schema: объект схемы
        :return: None
        """
        query = self.config.get('UPLOADING', 'schema')
        self.cursor.execute(query, {
                                    'name': schema.name,
                                    'fulltext_engine': schema.fulltext_engine,
                                    'version': schema.version,
                                    'description': schema.description
                                    }
                            )

    def upload_domain(self, domain: Domain):
        """ Выгрузить данные из объекта домена во временный источник доменов.

        :param domain: объект домена
        :return: None
        """
        query = self.config.get('UPLOADING', 'domain')
        self.cursor.execute(query, {
                                    'name': domain.name,
                                    'description': domain.description,
                                    'data_type_name': domain.type,
                                    'length': domain.length,
                                    'char_length': domain.char_length,
                                    'precision': domain.precision,
                                    'scale': domain.scale,
                                    'width': domain.width,
                                    'align': domain.align,
                                    'show_null': domain.show_null,
                                    'show_lead_nulls': domain.show_lead_nulls,
                                    'thousands_separator': domain.thousands_separator,
                                    'summable': domain.summable,
                                    'case_sensitive': domain.case_sensitive,
                                    'uuid': uuid.uuid1().hex
                                    }
                            )

    def upload_table(self, table: Table, schema: Schema):
        """ Выгрузить данные из объекта таблицы во временный источник таблиц.

        :param table: объект таблицы
        :param schema: объект схемы
        :return: None
        """
        query = self.config.get('UPLOADING', 'table')
        self.cursor.execute(query, {
                                    'schema_name': schema.name,
                                    'name': table.name,
                                    'description': table.description,
                                    'can_add': table.add,
                                    'can_edit': table.edit,
                                    'can_delete': table.delete,
                                    'temporal_mode': table.temporal_mode,
                                    'means': table.means,
                                    'uuid': uuid.uuid1().hex
                                    }
                            )

    def upload_field(self, field: Field, table: Table):
        """ Выгрузить данные из объекта поля во временный источник полей.

        :param field: объект поля
        :param table: объект таблицы
        :return: None
        """
        query = self.config.get('UPLOADING', 'field')
        self.cursor.execute(query, {
                                    'table_name': table.name,
                                    'position': list(table.fields.values()).index(field),
                                    'name': field.name,
                                    'russian_short_name': field.rname,
                                    'description': field.description,
                                    'domain_name': field.domain,
                                    'can_input': field.input,
                                    'can_edit': field.edit,
                                    'show_in_grid': field.show_in_grid,
                                    'show_in_details': field.show_in_details,
                                    'is_mean': field.is_mean,
                                    'autocalculated': field.autocalculated,
                                    'required': field.required,
                                    'uuid': uuid.uuid1().hex
                                    }
                            )

    def upload_constraint(self, constraint: Constraint, table: Table):
        """ Выгрузить данные из объекта ограничения во временный источника ограничений.

        :param constraint: объект ограничения
        :param table: объект таблицы
        :return: None
        """
        query = self.config.get('UPLOADING', 'constraint')
        self.cursor.execute(query, {
                                    'id': id(constraint),
                                    'table_name': table.name,
                                    'name': constraint.name,
                                    'constraint_type': constraint.kind,
                                    'reference': constraint.reference,
                                    'unique_key_name': constraint.constraint,
                                    'has_value_edit': constraint.has_value_edit,
                                    'cascading_delete': constraint.cascading_delete,
                                    'expression': constraint.expression,
                                    'uuid': uuid.uuid1().hex
                                    }
                            )

    def upload_index(self, index: Index, table: Table):
        """ Выгрузить данные из объекта индекса во временный источник индексов.

        :param index: объект индекса
        :param table: объект таблицы
        :return: None
        """
        query = self.config.get('UPLOADING', 'index')
        self.cursor.execute(query, {
                                    'id': id(index),
                                    'table_name': table.name,
                                    'name': index.name,
                                    'local': index.local,
                                    'kind': index.kind,
                                    'uuid': uuid.uuid1().hex
                                    }
                            )

    def upload_constraint_detail(self, detail: ConstraintDetail, constraint: Constraint):
        """ Выгрузить данные из объекта детали ограничения во временный источник деталей ограничений.

        :param detail: объект детали ограничения.
        :param constraint: объект ограничения.
        :return: None
        """
        query = self.config.get('UPLOADING', 'constraint_detail')
        self.cursor.execute(query, {
                                    'constraint_id': id(constraint),
                                    'position': constraint.details.index(detail),
                                    'field_name': detail.value
                                    }
                            )

    def upload_index_detail(self, detail: IndexDetail, index: Index):
        """ Выгрузить данные из объекта детали индекса во временный источник деталей индексов.

        :param detail: объект детали индекса
        :param index: объект индекса
        :return: None
        """
        query = self.config.get('UPLOADING', 'index_detail')
        self.cursor.execute(query, {
                                    'index_id': id(index),
                                    'position': index.details.index(detail),
                                    'field_name': detail.value,
                                    'expression': detail.expression,
                                    'descend': detail.descend
                                    }
                            )


def upload(schemas: list, db_file: str):
    """ Произвести выгрузку RAM-представления, передаваемого в виде списка схем, в базу SQLite по указанному пути,
    сформировав тем самым DBD-представление схемы БД.

    :param schemas: список объектов схем
    :param db_file: путь к файлу базы данных
    :return: None
    """
    conn = DbdUploadConnection('dbd_queries_sqlite.cfg', db_file)
    conn.create_dbd_repr()
    conn.create_tmp_dbd_repr()

    conn.cursor.executescript(BEGIN_TRANSACTION)

    for schema in schemas:
        conn.upload_schema(schema)
        for domain in schema.domains.values():
            conn.upload_domain(domain)
        for table in schema.tables.values():
            conn.upload_table(table, schema)
            for field in table.fields.values():
                conn.upload_field(field, table)
            for constraint in table.constraints:
                conn.upload_constraint(constraint, table)
                for detail in constraint.details:
                    conn.upload_constraint_detail(detail, constraint)
            for index in table.indexes:
                conn.upload_index(index, table)
                for detail in index.details:
                    conn.upload_index_detail(detail, index)

    conn.cursor.execute(COMMIT)

    conn.fill_main_tables()

