"""
Модуль, содержащий реализации класоов представления базы в RAM.
"""

import exceptions


class Schema:
    """
    Класс, моделирующий схему базы.
    """
    def __init__(self):
        self.attributes = dict(fulltext_engine=None,
                               version=None,
                               name=None,
                               description=None
                               )
        self.domains = {}
        self.tables = {}
        self.data_types = (
            'STRING', 'SMALLINT', 'INTEGER', 'WORD', 'BOOLEAN', 'FLOAT', 'CURRENCY', 'BCD', 'FMTBCD', 'DATE', 'TIME',
            'DATETIME', 'TIMESTAMP', 'BYTES', 'VARBYTES', 'BLOB', 'MEMO', 'GRAPHIC', 'FMTMEMO', 'FIXEDCHAR', 'BYTE',
            'WIDESTRING', 'LARGEINT', 'COMP', 'ARRAY', 'FIXEDWIDECHAR', 'WIDEMEMO', 'CODE', 'RECORDID', 'SET', 'PERIOD'
        )

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидацию объекта схемы.
        :return: None
        """
        if self.get('name') is None:
            raise exceptions.EmptyRequiredPropertyError('Имя схемы не задано.')


class Domain:
    """
    Класс, реализующий представление домена в RAM.
    """
    def __init__(self, schema):
        self.schema = schema
        self.attributes = dict(name=None,
                               description=None,
                               type=None,
                               align=None,
                               width=None,
                               length=None,
                               precision=None,
                               case_sensitive=False,
                               show_null=False,
                               show_lead_nulls=False,
                               thousands_separator=False,
                               summable=False,
                               char_length=None,
                               scale=None
                              )

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидацию объекта домена базы.
        :return: None
        """
        if self.get('name') is None:
            raise exceptions.EmptyRequiredPropertyError('Не задано имя домена.')
        if self.get('type') is None:
            raise exceptions.EmptyRequiredPropertyError('Не задан тип домена ' + str(self.get('name')))
        if self.get('type') not in self.schema.data_types:
            raise exceptions.UnsupportedDataTypeError('Неверно задан тип домена ' + str(self.get('name')))
        if self.get('name') in self.schema.domains.keys():
            raise exceptions.UniqueViolationError('Домен с именем ' + str(self.get('name')) + ' уже есть.')
        self.schema.domains[self.get('name')] = self


class Table:
    """
    Класс, моделирующий таблицу базы в RAM.
    """
    def __init__(self, schema):
        self.schema = schema
        self.attributes = dict(name=None,
                               description=None,
                               add=False,
                               edit=False,
                               delete=False,
                               ht_table_flags=None,
                               temporal_mode=None,
                               means=None,
                               access_level=None,
                               )
        self.fields = {}
        self.indexes = []
        self.constraints = []

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидацию объекта таблицы.
        :return: None
        """
        if self.get('name') is None:
            raise exceptions.EmptyRequiredPropertyError('Имя таблицы не задано.')
        if self.get('name') in self.schema.tables:
            raise exceptions.UniqueViolationError('Таблица ' + str(self.get('name')) + ' уже определена.')
        self.schema.tables[self.get('name')] = self


class Field:
    """
    Класс, моделирующий поле базы в RAM.
    """
    def __init__(self, table):
        self.table = table
        self.position = -1
        self.attributes = dict(name=None,
                               rname=None,
                               domain=None,
                               type=None,
                               description=None,
                               input=False,
                               edit=False,
                               show_in_grid=False,
                               show_in_details=False,
                               is_mean=False,
                               autocalculated=False,
                               required=False
                               )
        self.domain = None

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидацию объекта поля базы.
        :return: None
        """
        if self.attributes['name'] is None:
            raise exceptions.EmptyRequiredPropertyError('Не задано имя поля')
        if self.get('name') in self.table.fields:
            raise exceptions.UniqueViolationError('Поле' + str(self.get('name')) + ' уже определено.')
        if self.attributes['domain'] is None and self.attributes['type'] is None:
            raise exceptions.EmptyRequiredPropertyError('Не заданы домен и тип поля ' + str(self.get('name')))
        if self.attributes['domain'] is not None and self.get('domain') not in self.table.schema.domains:
            raise exceptions.ReferenceError('Неверно задан домен поля ' + str(self.get('name')))
        if self.attributes['type'] is not None and self.get('type') not in self.table.schema.data_types:
            raise exceptions.ReferenceError('Неверно задан тип поля ' + str(self.get('name')))
        self.domain = self.table.schema.domains[self.get('domain')]
        self.table.fields[self.get('name')] = self
        self.position = len(self.table.fields) + 1


class Constraint:
    """
    Класс, моделирующий ограничение базы в RAM.
    """
    def __init__(self, table):
        self.table = table
        self.attributes = dict(name=None,
                               kind=None,
                               items=None,
                               reference=None,
                               constraint=None,
                               has_value_edit=False,
                               cascading_delete=False,
                               full_cascading_delete=False,
                               expression=None
                               )
        self.details = []
        self.table.constraints.append(self)

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидацию объекта ограничения базы.
        :return: None
        """
        if 'kind' not in self.attributes:
            raise exceptions.EmptyRequiredPropertyError('Не задан тип ограничения таблицы.')
        elif self.get('kind') == 'PRIMARY' \
                and any([key for key in self.table.constraints if key.get('kind') == 'PRIMARY' and key != self]):
            raise exceptions.UniqueViolationError('Определено более одного первичного ключа.')
        elif self.get('kind') != 'FOREIGN' \
                and (self.attributes['reference'] is not None or self.attributes['constraint'] is not None):
            raise exceptions.ReferenceError('Ограничение, не являющееся внешним ключом, имеет ссылку')
        elif self.attributes['reference'] is not None and not self.get('reference') in self.table.schema.tables:
            raise exceptions.ReferenceError('Ограничение имеет ссылку на несуществующую таблицу')
        elif self.attributes['items'] is not None and not self.get('items') in self.table.fields:
            raise exceptions.ReferenceError('Ограничение задано на несуществующее поле')


class ConstraintDetail:
    """
    Класс, моделирующий деталь ограничения базы в RAM.
    """
    def __init__(self, constraint):
        self.constraint = constraint
        self.position = len(self.constraint.details) + 1
        self.attributes = dict(value=None)
        self.constraint.details.append(self)

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидацию объекта детали ограничения.
        :return: None
        """
        if 'value' not in self.attributes:
            raise exceptions.EmptyRequiredPropertyError('Не задано значение детали ограничения')
        elif self.get('value') not in self.constraint.table.schema.tables[self.constraint.get('reference')].fields:
            raise exceptions.ReferenceError('Деталь ограничения ссылается на несуществующее поле')


class Index:
    """
    Класс, моделирующий представление индекса базы в RAM.
    """
    def __init__(self, table):
        self.table = table
        self.attributes = dict(name=None,
                               field=None,
                               local=False,
                               uniqueness=False,
                               fulltext=False
                               )
        self.details = []
        self.table.indexes.append(self)

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидацию объекта индекса.
        :return: None
        """
        if self.attributes['field'] is not None and self.get('field') not in self.table.fields:
            raise exceptions.ReferenceError('Индекс ссылается на несуществующее поле.')


class IndexDetail:
    """
    Класс, моделирующий деталь индекса в базе.
    """
    def __init__(self, index):
        self.index = index
        self.attributes = dict(value=None,
                               uniqueness=False,
                               fulltext=False,
                               expression=None,
                               descend=None
                               )
        self.index.details.append(self)
        self.position = len(self.index.details)

    def get(self, attr):
        """
        Получить атрибут по его имени.
        :param attr: имя атрибута.
        :return: значеник атрибута.
        """
        return self.attributes[attr]

    def validate(self):
        """
        Произвести валидауию объекта детали индекса.
        :return: None
        """
        if 'value' not in self.attributes:
            raise exceptions.EmptyRequiredPropertyError('Не задано значение детали индекса.')
        if self.get('value') not in self.index.table.fields:
            raise exceptions.ReferenceError('Деталь индекса ссылается на несуществующее поле.')
