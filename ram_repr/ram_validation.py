""" Модуль, содержащий методы проверки корректности структуры Схема, представленной
в RAM в виде классов.
"""


from ram_repr.ram_structure import Constraint
from ram_repr.ram_structure import ConstraintDetail
from ram_repr.ram_structure import Domain
from ram_repr.ram_structure import Field
from ram_repr.ram_structure import Index
from ram_repr.ram_structure import IndexDetail
from ram_repr.ram_structure import Schema
from ram_repr.ram_structure import Table


def validate_schema(schema: Schema):
    """ Проверить корректность данных схемы (произвести валидацию)

    :param schema: объект схемы к валидации.
    :return: None
    """
    try:
        # Выполняется валидация объекта схемы.
        _validate_schema(schema)
        # Выполняется валидация каждой из таблиц схемы.
        for table in schema.tables.values():
            try:
                _validate_table(table)
                for field in table.fields.values():
                    try:
                        _validate_field(field, schema)
                    except ValidationError as err:
                        raise ValidationError('Поле.' + str(err))
                # Выполняется валидация каждого ограничения таблицы.
                for constraint in table.constraints:
                    try:
                        _validate_constraint(constraint, table, schema)
                        # Выполняется валидация деталей ограничения.
                        for detail in constraint.details:
                            try:
                                _validate_constraint_detail(detail, table)
                            except ValidationError as ex:
                                raise ValidationError('Деталь ограничения.' + str(ex))
                    except ValidationError as ex:
                        raise ValidationError('Ограничение.' + str(ex))
                # Выполняется валидация каждого индекса таблицы.
                for index in table.indexes:
                    try:
                        _validate_index(index, table)
                        # Выполняется валидация деталей индекса.
                        for detail in index.details:
                            try:
                                _validate_index_detail(detail, table)
                            except ValidationError as ex:
                                raise ValidationError('Деталь индекса.' + str(ex))  # Производится
                    except ValidationError as ex:                                   # каскадный
                        raise ValidationError('Индекс. ' + str(ex))                 # проброс
            except ValidationError as ex:                                           # исключений.
                raise ValidationError('Таблица ' + str(table.name) + '. ' + str(ex))
    except ValidationError as ex:
        raise ValidationError('Схема ' + str(schema.name) + '. ' + str(ex))


def _validate_schema(schema: Schema):
    """ Произвести валидацию объекта схемы.

    :return: None
    """
    if schema.name is None:
        raise EmptyRequiredPropertyError('name')


def _validate_domain(domain: Domain, schema: Schema):
    """ Произвести валидацию объекта домена базы.

    :return: None
    """
    if domain.name is None:
        raise EmptyRequiredPropertyError('name')
    if domain.type is None:
        raise EmptyRequiredPropertyError('type')
    if domain.type not in schema.data_types:
        raise UnsupportedDataTypeError(domain.type)


def _validate_table(table: Table):
    """ Произвести валидацию объекта таблицы.

    :return: None
    """
    if table.name is None:
        raise EmptyRequiredPropertyError('name')


def _validate_field(field: Field, schema: Schema):
    """ Произвести валидацию объекта поля базы.

    :return: None
    """
    if field.name is None:
        raise EmptyRequiredPropertyError('name')
    if field.domain is None and field.type is None:
        raise EmptyRequiredPropertyError('domain, type')
    if field.type is not None and field.type not in schema.data_types:
        raise UnsupportedDataTypeError(field.type)
    if field.domain is not None and field.domain not in schema.domains:
        raise ElementReferenceError(field.domain)


def _validate_constraint(constraint: Constraint, table: Table, schema: Schema):
    """ Произвести валидацию объекта ограничения базы.

    :return: None
    """
    if constraint.kind is None:
        raise EmptyRequiredPropertyError('kind')
    elif constraint.kind == 'PRIMARY' \
            and any([key for key in table.constraints if key.kind == 'PRIMARY' and key != constraint]):
        raise UniqueViolationError('PRIMARY')
    elif constraint.kind != 'FOREIGN' \
            and (constraint.reference is not None or constraint.constraint is not None):
        raise ForeignKeyError()
    elif constraint.reference is not None and constraint.reference not in schema.tables:
        raise ElementReferenceError(constraint.reference)


def _validate_constraint_detail(detail: ConstraintDetail, table: Table):
    """ Произвести валидацию объекта детали ограничения.

    :return: None
    """
    if detail.value is None:
        raise EmptyRequiredPropertyError('value')
    elif detail.value not in table.fields:
        raise ElementReferenceError(detail.value)


def _validate_index(index: Index, table: Table):
    """ Произвести валидацию объекта индекса.

    :return: None
    """
    pass


def _validate_index_detail(detail: IndexDetail, table: Table):
    """ Произвести валидауию объекта детали индекса.

    :return: None
    """
    if detail.value is None:
        raise EmptyRequiredPropertyError('value')
    if detail.value not in table.fields:
        raise ElementReferenceError(detail.value)


class ValidationError(Exception):
    """ Подкласс исключений, порождаемых в процессе валидации схемы.
    """
    pass


class EmptyRequiredPropertyError(ValidationError):
    """ Подкласс исключений, порождаемых в случае отсутствия определения обязательных
    свойств в структуре схемы.
    """
    def __init__(self, prop):
        self.prop = prop

    def __str__(self):
        return 'Не определено обязательное свойство \"' + self.prop + '\"'


class UnsupportedDataTypeError(ValidationError):
    """ Подкласс исключений, порождаемых в случае использования неподдерживаемых
    типов данных.
    """
    def __init__(self, _type):
        self.type = _type

    def __str__(self):
        return 'Задан неподдерживаемый тип данных \"' + self.type + '\"'


class ElementReferenceError(ValueError):
    """ Подкласс иключений, порождемых в случае обнаружения ссылок на неопределенные
    элементы Схемы.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Задана ссылка на неопределенный элемент \"' + self.name + '\"'


class UniqueViolationError(ValidationError):
    """ Подкласс исключений, порождаемых в случае нарушения уникальности элементов
    в разрезе некоторого свойства.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Элемент заданного типа с именем \"' + self.name + '\" уже определен'


class ForeignKeyError(ValidationError):
    """ Подкласс исключений, порождаемых в случае некорректного задания структуры
    Ограничения "Внешний ключ".
    """
    def __str__(self):
        return 'Неверная структура ограничения "Внешний ключ"'
