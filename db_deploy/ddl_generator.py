""" Модуль, содержащий методы генерации DDL-инструкций для PostgreSQL
из RAM-представления схемы БД, основываясь на шаблонах из файла.
"""
import configparser
import string

from ram_repr.ram_structure import Constraint
from ram_repr.ram_structure import Domain
from ram_repr.ram_structure import Field
from ram_repr.ram_structure import Index
from ram_repr.ram_structure import Schema
from ram_repr.ram_structure import Table


class DdlGenerator:
    """ Класс-генератор DDL-инструкций для создания элеменов БД, исходя из представления
    метаданных в ОП.
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = open('../ddl_templates.cfg', encoding='utf-8')
        self.config.read_file(self.config_file)
        self.templates = self.config['TEMPLATES']

    def __exit__(self):
        self.config_file.close()

    def create_schema_dll(self, schema: Schema):
        """ Создать DDL-инструкцию создания схемы в базу PostgreSQL.

        :param schema: объект схемы.
        :return: str
        """
        return string.Template(self.templates.get('schema'))\
            .substitute(
                        schema_name=schema.name
                        )

    def create_domain_dll(self, domain: Domain, schema: Schema):
        """ Создать DDL-инструкцию создания схемы в базе PostgreSQL.

        :param domain: объект домена
        :param schema: объект схемы
        :return: str
        """
        return string.Template(self.templates.get('domain'))\
            .substitute(
                        schema_name=schema.name,
                        domain_name=domain.name,
                        data_type=self._get_postgres_type(domain),
                        description=domain.description
                        )

    def create_table_ddl(self, table: Table, schema: Schema):
        """ Создать DDL-инструкцию создания таблицы в базе данных PostgreSQL.

        :param table: объект таблицы.
        :param schema: объект схемы.
        :return: str
        """
        fields = '\n,'.join(
                                [
                                    self.create_field_ddl(field, schema)
                                    for field in table.fields.values()
                                ]
                            )
        return string.Template(self.templates.get('table'))\
            .substitute(
                        schema_name=schema.name,
                        table_name=table.name,
                        fields=fields
                        )

    def create_field_ddl(self, field: Field, schema: Schema):
        """ Создать DDL-инструкцию дял создания поля в БД.

        :param field: объект поля.
        :param schema: объект схемы.
        :return: str
        """
        return string.Template(self.templates.get('field'))\
            .substitute(
                        field_name=field.name,
                        field_type=field.domain,
                        schema_name=schema.name
                        )

    def create_constraint_ddl(self, constraint: Constraint, table: Table, schema: Schema):
        """ Создать DDL-инструкцию для создания ограничения в БД.

        :param constraint: объект ограничения.
        :param table: объект таблицы.
        :param schema: объект схемы.
        :return: str
        """
        details = []
        for det in constraint.details:
            detail = r'"' + det.value + r'"'
            details.append(detail)

        if constraint.kind.upper() == 'PRIMARY':
            definition = string.Template(self.templates.get('primary'))\
                .substitute(
                            values=', '.join(details)
                            )

        elif constraint.kind.upper() == 'FOREIGN':
            definition = string.Template(self.templates.get('foreign'))\
                .substitute(
                            values=', '.join(details),
                            reference_schema=schema.name,
                            reference_table=constraint.reference,
                            constraint_name=constraint.name if constraint.name else ''
                            )
        else:
            return ''

        return string.Template(self.templates.get('constraint'))\
            .substitute(
                schema_name=schema.name,
                table_name=table.name,
                constraint_definition=definition
                )

    def create_index_ddl(self, index: Index, table: Table, schema: Schema):
        """ Создать DDL-инструкцию для создания индекса в БД.

        :param index: объект индекса.
        :param table: объект таблицы.
        :param schema: объект схемы.
        :return: str
        """
        details = []
        for det in index.details:
            detail = r'"' + det.value + r'"'
            if det.expression:
                detail += ' (' + det.expression + ')'
            if not det.descend:
                detail += ' ASC'
            else:
                detail += det.descend.upper()
            details.append(detail)

        if len(details) == 0:
            return ''

        return string.Template(self.templates.get('index'))\
            .substitute(
                        index_name='"' + index.name + table.name + '"' if index.name else '',
                        table_name=table.name,
                        schema_name=schema.name,
                        fields=', '.join(details)
                        )

    def _get_postgres_type(self, domain):
        """ Получить строку, представляющую тип домена представления метаданны в ОП.

        :param domain: объект домена.
        :return: str
        """
        if domain.type.upper() in ['STRING', 'MEMO', 'SYSNAME', 'NVARCHAR', 'VARCHAR']:
            if domain.char_length and int(domain.char_length) > 0:
                return string.Template(self.templates.get('domain_type'))\
                    .substitute(
                                type_name='varchar',
                                props=domain.char_length
                                )
            else:
                return 'varchar'
        elif domain.type.upper() in ['UNIQUEIDENTIFIER', 'MONEY', 'SQL_VARIANT', 'BIT']:
            return 'varchar(200)'
        elif domain.type.upper() in ['NTEXT', 'NCHAR', 'CHAR', 'BLOB', 'VARBINARY', 'BINARY', 'IMAGE']:
            return 'text'
        elif domain.type.upper() == 'BOOLEAN':
            return 'BOOLEAN'
        elif domain.type.upper() == 'DATE':
            return 'date'
        elif domain.type.upper() == 'TIME':
            return 'time'
        elif domain.type.upper() in ['LARGEINT', 'CODE', 'BIGINT']:
            return 'bigint'
        elif domain.type.upper() in ['WORD', 'BYTE', 'SMALLINT', 'INT', 'TINYINT']:
            return 'INTEGER'
        elif domain.type.upper() in ['FLOAT', 'REAL']:
            return 'REAL'
        elif domain.type.upper() in ['DATETIME']:
            return 'timestamp'
        print(domain.type.upper())
        return ''
