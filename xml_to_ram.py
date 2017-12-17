from xml.dom.minidom import parse

from ram_structure import Constraint
from ram_structure import ConstraintDetail
from ram_structure import Domain
from ram_structure import Field
from ram_structure import Index
from ram_structure import IndexDetail
from ram_structure import Schema
from ram_structure import Table
from ram_validation import validate_schema


def read(path):
    """ Считать модель базы из XML-файла.

    :param path: путь к XML-файлу с текстовым представлением базы.
    :return: список схем базы (на случай, если их более 1)
    """
    schemas = []
    dom = parse(path)
    for child in dom.childNodes:
        if child.tagName == 'dbd_schema':
            schema = _parse_schema(child)
            validate_schema(schema)
            schemas.append(schema)
        else:
            raise UnsupportedTagError(child.tagName)
    return schemas


def _parse_schema(dom_schema):
    """ Преобразовать dom-структуру, представляющу схему базы, в объект.

    :param dom_schema: dom-структура схемы.
    :return: объект схемы.
    """
    try:
        schema = _create_schema(dom_schema._attrs)
    except UnsupportedAttributeError as ex:
        raise ParseError('Не удалось создать схему. ' + str(ex))
    try:
        for child in dom_schema.childNodes:
            if _check_node(child):
                continue
            if child.tagName == 'domains':
                _parse_domain(schema, child)
            elif child.tagName == 'tables':
                _parse_table(schema, child)
            elif child.tagName != 'custom':
                raise UnsupportedTagError(child.tagName)
    except ParseError as ex:
        raise ParseError('Схема ' + schema.name + ': ' + str(ex))
    return schema


def _parse_domain(schema, dom):
    """ Преобразовать список dom-элементов, представляющих домены, в список доменов схемы.

    :param schema: схема, содержащая получаемые домены.
    :param dom: список dom-объектов доменов.
    :return: None
    """
    domains = dom.childNodes
    try:
        for domain_element in domains:
            if _check_node(domain_element):
                continue
            if domain_element.tagName != 'domain':
                raise UnsupportedTagError(domain_element.tagName)
            domain = _create_domain(domain_element._attrs)
            if domain.name in schema.domains:
                raise UniqueViolationError(domain.name)
            schema.domains[domain.name] = domain
    except ParseError as ex:
        raise ParseError('Домен. ' + str(ex))


def _parse_table(schema, dom):
    """ Проебразовать список dom-элементов, представляющих таблицы, в список таблиц схемы.

    :param schema: схема, содержащая получаемые таблицы.
    :param dom: список dom-объектов таблиц.
    :return: None
    """
    tables = dom.childNodes
    for table_element in tables:
        if _check_node(table_element):
            continue
        if table_element.tagName != 'table':
            raise UnsupportedTagError(table_element.tagName)
        table = _create_table(table_element._attrs)
        if table.name in schema.tables:
            raise UniqueViolationError(table.name)
        schema.tables[table.name] = table

        try:
            for child in table_element.childNodes:
                if _check_node(child):
                    continue
                if child.tagName == 'field':
                    field = _create_field(child._attrs)
                    if field.name in table.fields:
                        raise UniqueViolationError(field.name)
                    table.fields[field.name] = field

                elif child.tagName == 'index':
                    index = _create_index(child._attrs)
                    table.indexes.append(index)
                    for detail_node in child.childNodes:
                        if _check_node(detail_node):
                            continue
                        if detail_node.tagName != 'item':
                            raise UnsupportedTagError(detail_node.tagName)
                        detail = _create_index_detail(detail_node._attrs)
                        index.details.append(detail)

                elif child.tagName == 'constraint':
                    constraint = _create_constraint(child._attrs)
                    table.constraints.append(constraint)
                    for detail_node in child.childNodes:
                        if _check_node(detail_node):
                            continue
                        if detail_node.tagName != 'item':
                            raise UnsupportedTagError(detail_node.tagName)
                        detail = _create_constraint_detail(detail_node._attrs)
                        constraint.details.append(detail)

                else:
                    raise UnsupportedTagError(table_element.tagName)
        except ParseError as ex:
            raise ParseError('Таблица: \"' + table.name + '\". ' + str(ex))


def _check_node(node):
    """ Проверить узел dom-структуры.

    :param node: узел к проверке.
    :return: исключение в случае непустого узла.
    """
    if node.nodeType == node.TEXT_NODE:
        if node.nodeValue.strip() != '':
            raise UnsupportedTagError(node.nodeValue)
        return True
    return False


def _create_schema(attr_dict):
    """ Создать объект Схемы, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Схемы.
    """
    schema = Schema()
    for attr in attr_dict:
        if attr == 'name':
            schema.name = attr_dict[attr].value
        elif attr == 'fulltext_engine':
            schema.fulltext_engine = attr_dict[attr].value
        elif attr == 'version':
            schema.version = attr_dict[attr].value
        elif attr == 'description':
            schema.description = attr_dict[attr].value
        else:
            raise UnsupportedAttributeError(attr)
    return schema


def _create_domain(attr_dict):
    """ Создать объект Домена, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Домена.
    """
    domain = Domain()
    for attr in attr_dict:
        if attr == 'name':
            domain.name = attr_dict[attr].value
        elif attr == 'type':
            domain.type = attr_dict[attr].value
        elif attr == 'align':
            domain.align = attr_dict[attr].value
        elif attr == 'width':
            domain.width = attr_dict[attr].value
        elif attr == 'char_length':
            domain.char_length = attr_dict[attr].value
        elif attr == 'description':
            domain.description = attr_dict[attr].value
        elif attr == 'length':
            domain.length = attr_dict[attr].value
        elif attr == 'scale':
            domain.scale = attr_dict[attr].value
        elif attr == 'precision':
            domain.precision = attr_dict[attr].value
        elif attr == 'props':
            for prop in attr_dict[attr].value.split(', '):
                if prop == 'case_sensitive':
                    domain.case_sensitive = True
                elif prop == 'show_null':
                    domain.show_null = True
                elif prop == 'show_lead_nulls':
                    domain.show_lead_nulls = True
                elif prop == 'thousands_separator':
                    domain.thousands_separator = True
                elif prop == 'summable':
                    domain.summable = True
                else:
                    raise UnsupportedPropertyError(prop)
        else:
            raise UnsupportedAttributeError(attr)
    return domain


def _create_table(attr_dict):
    """ Создать объект Таблицы, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Таблицы.
    """
    table = Table()
    for attr in attr_dict:
        if attr == 'name':
            table.name = attr_dict[attr].value
        elif attr == 'description':
            table.description = attr_dict[attr].value
        elif attr == 'props':
            for prop in attr_dict[attr].value.split(', '):
                if prop == 'add':
                    table.add = True
                elif prop == 'edit':
                    table.edit = True
                elif prop == 'delete':
                    table.delete = True
                else:
                    raise UnsupportedPropertyError(prop)
        else:
            raise UnsupportedAttributeError(attr)
    return table


def _create_field(attr_dict):
    """ Создать объект Поля, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Поля.
    """
    field = Field()
    for attr in attr_dict:
        if attr == 'name':
            field.name = attr_dict[attr].value
        elif attr == 'rname':
            field.rname = attr_dict[attr].value
        elif attr == 'domain':
            field.domain = attr_dict[attr].value
        elif attr == 'type':
            field.type = attr_dict[attr].value
        elif attr == 'description':
            field.description = attr_dict[attr].value
        elif attr == 'props':
            for prop in attr_dict[attr].value.split(', '):
                if prop == 'input':
                    field.input = True
                elif prop == 'edit':
                    field.edit = True
                elif prop == 'show_in_grid':
                    field.show_in_grid = True
                elif prop == 'show_in_details':
                    field.show_in_details = True
                elif prop == 'is_mean':
                    field.is_mean = True
                elif prop == 'autocalculated':
                    field.autocalculated = True
                elif prop == 'required':
                    field.required = True
                else:
                    raise UnsupportedPropertyError(prop)
        else:
            raise UnsupportedAttributeError(attr)
    return field


def _create_constraint(attr_dict):
    """ Создать объект Ограничения, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Ограничения.
    """
    constraint = Constraint()

    if attr_dict is None:
        return constraint

    for attr in attr_dict:
        if attr == 'name':
            constraint.name = attr_dict[attr].value
        elif attr == 'kind':
            constraint.kind = attr_dict[attr].value
        elif attr == 'items':
            detail = ConstraintDetail()
            detail.value = attr_dict[attr].value
            constraint.details.append(detail)
        elif attr == 'reference':
            constraint.reference = attr_dict[attr].value
        elif attr == 'constraint':
            constraint.constraint = attr_dict[attr].value
        elif attr == 'expression':
            constraint.expression = attr_dict[attr].value
        elif attr == 'props':
            for prop in attr_dict[attr].value.split(', '):
                if prop == 'has_value_edit':
                    constraint.has_value_edit = True
                elif prop == 'cascading_delete':
                    constraint.cascading_delete = False
                elif prop == 'full_cascading_delete':
                    constraint.cascading_delete = True
                else:
                    raise UnsupportedPropertyError(prop)
        else:
            raise UnsupportedAttributeError(attr)
    return constraint


def _create_index(attr_dict):
    """ Создать объект Индекса, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Индекса.
    """
    index = Index()

    if attr_dict is None:
        return index

    for attr in attr_dict:
        if attr == 'name':
            index.name = attr_dict[attr].value
        elif attr == 'field':
            detail = IndexDetail()
            detail.value = attr_dict[attr].value
            index.details.append(detail)
        elif attr == 'props':
            for prop in attr_dict[attr].value.split(', '):
                if prop == 'local':
                    index.local = True
                elif prop == 'uniqueness':
                    index.kind = 'uniqueness'
                elif prop == 'fulltext':
                    index.kind = 'fulltext'
                else:
                    raise UnsupportedPropertyError(prop)
        else:
            raise UnsupportedAttributeError(attr)
    return index


def _create_constraint_detail(attr_dict):
    """ Создать объект Детали ограничения, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Детали ограничения.
    """
    detail = ConstraintDetail()
    for attr in attr_dict:
        if attr == 'value':
            detail.value = attr_dict[attr].value
        else:
            raise UnsupportedAttributeError(attr)
    return detail


def _create_index_detail(attr_dict):
    """ Создать объект Детали индекса, опредлить его поля.

    :param attr_dict: Словарь свойств из dom-элемента.
    :return: объект Детали индекса.
    """
    detail = IndexDetail()
    for attr in attr_dict:
        if attr == 'value':
            detail.value = attr_dict[attr].value
        elif attr == 'expression':
            detail.expression = attr_dict[attr].value
        elif attr == 'descend':
            detail.descend = attr_dict[attr].value
        else:
            raise UnsupportedAttributeError(attr)
    return detail


class ParseError(Exception):
    """ Подкласс исключений, порождаемых в процессе парсинга XML-представления
    схемы БД.
    """
    pass


class UnsupportedTagError(ParseError):
    """ Подкласс исключений, порождаемых при обнаружении неподдерживаемого тега
    в XML-представлении БД.
    """
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return 'Неподдерживаемый тэг \"' + self.tag + '\"'


class UnsupportedAttributeError(ParseError):
    """ Подкласс исключений, порождаемых при обнаружении неподдерживаемого
    атрибута в XML-представлении БД.
    """
    def __init__(self, attribute):
        self.attribute = attribute

    def __str__(self):
        return 'Неподдерживаемый атрибут \"' + self.attribute + '\"'


class UnsupportedPropertyError(ParseError):
    """ Подкласс исключений, порождаемых при обнаружении неподдерживаемого
    свойства в XML-представлении БД.
    """
    def __init__(self, prop):
        self.prop = prop

    def __str__(self):
        return 'Неподдерживаемое свойство \"' + self.prop + '\"'


class UniqueViolationError(ParseError):
    """ Подкласс исключений, порождаемых в случае нарушения уникальности
    имен некоторых элементов представления БД в виде XML.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Элемент заданного типа с именем \"' + self.name + '\" уже определен'