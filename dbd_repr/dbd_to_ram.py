import configparser
import pyodbc
import sqlite3

from ram_repr.ram_structure import Constraint
from ram_repr.ram_structure import ConstraintDetail
from ram_repr.ram_structure import Domain
from ram_repr.ram_structure import Field
from ram_repr.ram_structure import Index
from ram_repr.ram_structure import IndexDetail
from ram_repr.ram_structure import Schema
from ram_repr.ram_structure import Table


class DbdDownloadConnection:
    """ Класс, реализующий подключеине к базе для загрузки данных из источников структурных
    элементов в виде словарей.
    """
    def __init__(self, queries_config: str, db_file=None):
        self.queries = configparser.ConfigParser()
        self.queries.read(queries_config, 'utf-8')
        if db_file:
            self.conn = sqlite3.connect(db_file)
        else:
            server = self.queries.get('SERVER', 'server')
            self.conn = pyodbc.connect(server)
        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.conn.close()

    def _get_result(self):
        """ Получить результат последнего выполненного запроса в виде словаря.

        :return: dict
        """
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def load_schemas(self):
        """ Загрузить словари схем.

        :return: dict
        """
        query = self.queries.get('DOWNLOADING', 'schema')
        self.cursor.execute(query)
        return self._get_result()

    def load_domains(self):
        """ Загрузить словари доменов.

        :return: dict
        """
        query = self.queries.get('DOWNLOADING', 'domain')
        self.cursor.execute(query)
        return self._get_result()

    def load_tables(self):
        """ Загрузить словари таблиц.

        :return: dict
        """
        query = self.queries.get('DOWNLOADING', 'table')
        self.cursor.execute(query)
        return self._get_result()

    def load_fields(self):
        query = self.queries.get('DOWNLOADING', 'field')
        self.cursor.execute(query)
        return self._get_result()

    def load_constraints(self):
        """ Загрузить словари ограничений.

        :return: dict
        """
        query = self.queries.get('DOWNLOADING', 'constraint')
        self.cursor.execute(query)
        return self._get_result()

    def load_index(self):
        """ Загрузить словари индексов.

        :return: dict
        """
        query = self.queries.get('DOWNLOADING', 'index')
        self.cursor.execute(query)
        return self._get_result()

    def load_constraint_details(self):
        """ Загрузить словари деталей ограничений.

        :return: dict
        """
        query = self.queries.get('DOWNLOADING', 'constraint_detail')
        self.cursor.execute(query)
        return self._get_result()

    def load_index_details(self):
        """ Загрузить словари деталей индексов.

        :return: dict
        """
        query = self.queries.get('DOWNLOADING', 'index_detail')
        self.cursor.execute(query)
        return self._get_result()


def load(queries: str, db_file: str=None):
    """ Создать RAM-представление схемы базы посредствам загрузки струтурных компонентов из базы,
    получаемой из файла, путь к которому передается в качестве параметра.

    :param queries: путь к файлу с параметрами подключения и запросами.
    :param db_file: путь к файлу базы данных
    :return: listW
    """
    conn = DbdDownloadConnection(queries, db_file)

    schemas = {}
    for schema_row in conn.load_schemas():
        schema, schema_id = _create_schema(schema_row)
        schemas[schema_id] = schema

    tables = {}
    for table_row in conn.load_tables():
        table, table_id, schema_id = _create_table(table_row)
        tables[table_id] = table
        schemas[schema_id].tables[table.name] = table

    domains = {}
    for domain_row in conn.load_domains():
        domain, domain_id = _create_domain(domain_row)
        domains[domain_id] = domain
        for schema in [schema for schema in schemas.values() if len(schema.tables) > 0]:
            schema.domains[domain.name] = domain

    fields = {}
    for field_row in conn.load_fields():
        field, field_id, table_id = _create_field(field_row)
        if table_id not in tables:
            continue
        tables[table_id].fields[field.name] = field
        fields[field_id] = field

    constraints = {}
    for constraint_row in conn.load_constraints():
        constraint, constraint_id, table_id = _create_constraint(constraint_row)
        if table_id not in tables:
            continue
        tables[table_id].constraints.append(constraint)
        constraints[constraint_id] = constraint

    indices = {}
    for index_row in conn.load_index():
        index, index_id, table_id = _create_index(index_row)
        if table_id not in tables:
            continue
        tables[table_id].indexes.append(index)
        indices[index_id] = index

    constraint_details = {}
    for detail_row in conn.load_constraint_details():
        detail, detail_id, constraint_id = _create_constraint_detail(detail_row)
        constraints[constraint_id].details.append(detail)
        constraint_details[detail_id] = detail

    index_details = {}
    for detail_row in conn.load_index_details():
        detail, detail_id, index_id = _create_index_detail(detail_row)
        if index_id not in indices:
            continue
        indices[index_id].details.append(detail)
        index_details[detail_id] = detail

    return schemas.values()


def _create_schema(attr_dict):
    """ Создать объект Схемы, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Схемы.
    """
    schema = Schema()

    schema_id = None

    for attr in attr_dict:
        if attr == 'name':
            schema.name = attr_dict[attr]
        elif attr == 'fulltext_engine':
            schema.fulltext_engine = attr_dict[attr]
        elif attr == 'version':
            schema.version = attr_dict[attr]
        elif attr == 'description':
            schema.description = attr_dict[attr]
        elif attr == 'id':
            schema_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return schema, schema_id


def _create_domain(attr_dict):
    """ Создать объект Домена, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Домена.
    """
    domain = Domain()

    domain_id = None

    for attr in attr_dict:
        if attr == 'name':
            domain.name = attr_dict[attr]
        elif attr == 'data_type_name':
            domain.type = attr_dict[attr]
        elif attr == 'align':
            domain.align = attr_dict[attr]
        elif attr == 'width':
            domain.width = attr_dict[attr]
        elif attr == 'char_length':
            domain.char_length = attr_dict[attr]
        elif attr == 'description':
            domain.description = attr_dict[attr]
        elif attr == 'length':
            domain.length = attr_dict[attr]
        elif attr == 'scale':
            domain.scale = attr_dict[attr]
        elif attr == 'precision':
            domain.precision = attr_dict[attr]
        elif attr == 'case_sensitive':
            domain.case_sensitive = attr_dict[attr]
        elif attr == 'show_null':
            domain.show_null = attr_dict[attr]
        elif attr == 'show_lead_nulls':
            domain.show_lead_nulls = attr_dict[attr]
        elif attr == 'thousands_separator':
            domain.thousands_separator = attr_dict[attr]
        elif attr == 'summable':
            domain.summable = attr_dict[attr]
        elif attr == 'id':
            domain_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return domain, domain_id


def _create_table(attr_dict):
    """ Создать объект Таблицы, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Таблицы.
    """
    table = Table()

    table_id = None
    schema_id = None

    for attr in attr_dict:
        if attr == 'name':
            table.name = attr_dict[attr]
        elif attr == 'description':
            table.description = attr_dict[attr]
        elif attr == 'temporal_mode':
            table.ht_table_flags = attr_dict[attr]
        elif attr == 'access_level':
            table.access_level = attr_dict[attr]
        elif attr == 'can_add':
            table.add = attr_dict[attr]
        elif attr == 'can_edit':
            table.edit = attr_dict[attr]
        elif attr == 'can_delete':
            table.delete = attr_dict[attr]
        elif attr == 'means':
            table.means = attr_dict[attr]
        elif attr == 'schema_id':
            schema_id = attr_dict[attr]
        elif attr == 'id':
            table_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return table, table_id, schema_id


def _create_field(attr_dict):
    """ Создать объект Поля, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Поля.
    """
    field = Field()

    field_id = None
    table_id = None

    for attr in attr_dict:
        if attr == 'name':
            field.name = attr_dict[attr]
        elif attr == 'russian_short_name':
            field.rname = attr_dict[attr]
        elif attr == 'domain_name':
            field.domain = attr_dict[attr]
        elif attr == 'type':
            field.type = attr_dict[attr]
        elif attr == 'description':
            field.description = attr_dict[attr]
        elif attr == 'can_input':
            field.input = attr_dict[attr]
        elif attr == 'can_edit':
            field.edit = attr_dict[attr]
        elif attr == 'show_in_grid':
            field.show_in_grid = attr_dict[attr]
        elif attr == 'show_in_details':
            field.show_in_details = attr_dict[attr]
        elif attr == 'is_mean':
            field.is_mean = attr_dict[attr]
        elif attr == 'autocalculated':
            field.autocalculated = attr_dict[attr]
        elif attr == 'required':
            field.required = attr_dict[attr]
        elif attr == 'id':
            field_id = attr_dict[attr]
        elif attr == 'table_id':
            table_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return field, field_id, table_id


def _create_constraint(attr_dict):
    """ Создать объект Ограничения, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Ограничения.
    """
    constraint = Constraint()

    if attr_dict is None:
        return constraint

    constraint_id = None
    table_id = None

    for attr in attr_dict:
        if attr == 'name':
            constraint.name = attr_dict[attr]
        elif attr == 'constraint_type':
            constraint.kind = attr_dict[attr]
        elif attr == 'items':
            detail = ConstraintDetail()
            detail.value = attr_dict[attr]
            constraint.details.append(detail)
        elif attr == 'reference':
            constraint.reference = attr_dict[attr]
        elif attr == 'unique_key_id':
            constraint.constraint = attr_dict[attr]
        elif attr == 'expression':
            constraint.expression = attr_dict[attr]
        elif attr == 'has_value_edit':
            constraint.has_value_edit = attr_dict[attr]
        elif attr == 'cascading_delete':
            constraint.cascading_delete = attr_dict[attr]
        elif attr == 'id':
            constraint_id = attr_dict[attr]
        elif attr == 'table_id':
            table_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return constraint, constraint_id, table_id


def _create_index(attr_dict):
    """ Создать объект Индекса, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Индекса.
    """
    index = Index()

    if attr_dict is None:
        return index

    index_id = None
    table_id = None

    for attr in attr_dict:
        if attr == 'name':
            index.name = attr_dict[attr]
        elif attr == 'field':
            detail = IndexDetail()
            detail.value = attr_dict[attr]
            index.details.append(detail)
        elif attr == 'kind':
            index.kind = attr_dict[attr]
        elif attr == 'local':
            index.local = attr_dict[attr]
        elif attr == 'uniqueness':
            index.uniqueness = attr_dict[attr]
        elif attr == 'fulltext':
            index.fulltext = attr_dict[attr]
        elif attr == 'id':
            index_id = attr_dict[attr]
        elif attr == 'table_id':
            table_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return index, index_id, table_id


def _create_constraint_detail(attr_dict):
    """ Создать объект Детали ограничения, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Детали ограничения.
    """
    detail = ConstraintDetail()

    detail_id = None
    constraint_id = None

    for attr in attr_dict:
        if attr == 'field_name':
            detail.value = attr_dict[attr]
        elif attr == 'id':
            detail_id = attr_dict[attr]
        elif attr == 'constraint_id':
            constraint_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return detail, detail_id, constraint_id


def _create_index_detail(attr_dict):
    """ Создать объект Детали индекса, опредлить его поля.

    :param attr_dict: Словарь свойств из dbd-представления.
    :return: объект Детали индекса.
    """
    detail = IndexDetail()

    detail_id = None
    index_id = None

    for attr in attr_dict:
        if attr == 'field_name':
            detail.value = attr_dict[attr]
        elif attr == 'expression':
            detail.expression = attr_dict[attr]
        elif attr == 'descend':
            detail.descend = attr_dict[attr]
        elif attr == 'id':
            detail_id = attr_dict[attr]
        elif attr == 'index_id':
            index_id = attr_dict[attr]
        else:
            raise UnsupportedAttributeError(attr)
    return detail, detail_id, index_id


class ParseError(Exception):
    """ Подкласс исключений, порождаемых в процессе парсинга DBD-представления
    схемы БД.
    """
    pass


class UnsupportedAttributeError(ParseError):
    """ Подкласс исключений, порождаемых при обнаружении неподдерживаемого
    атрибута в DBD-представлении БД.
    """
    def __init__(self, attribute):
        self.attribute = attribute

    def __str__(self):
        return 'Неподдерживаемый атрибут \"' + self.attribute + '\"'
