from structure import Schema
from structure import Domain
from structure import Table
from structure import Field
from structure import Index
from structure import Constraint
from structure import ConstraintDetail
from structure import IndexDetail
from xml.dom.minidom import parse
import exceptions


def read(path):
    """
    Считать модель базы из XML-файла.
    :param path: путь к XML-файлу с текстовым представлением базы.
    :return: список схем базы (на случай, если их более 1)
    """
    dom = parse(path)
    schemas = []
    try:
        for child in dom.childNodes:
            schemas.append(_parse_schema(child))
    except Exception as e:
        print(str(e))
    return schemas


def _check_node(node):
    """
    Проверить узел dom-структуры.
    :param node: узел к проверке.
    :return: признак того, что узел является незначимым (перенос или пробелы)
    """
    if node.nodeType == node.TEXT_NODE:
        if node.nodeValue.strip() == '':
            return True
        else:
            raise exceptions.UnsupportedTagError('Неподдерживаемый текстовый узел \"' + node.nodeValue + '\"')


def parse_attributes(attr_dict, attributes):
    """
    Преобразовать атрибуты dom-элемента в справочник, проверив их корректность.
    :param attr_dict: целевой справочник аттрибутов.
    :param attributes: исходный список атрибутов dom-элемента.
    :return: None
    """
    for attr in attributes.keys():
        if attr != 'props':
            if attr not in attr_dict:
                raise exceptions.UnsupportedAttributeError('Атрибут ' + attr + ' не поддерживается.')
            else:
                attr_dict[attr] = attributes.get(attr).value
        else:
            props = attributes.get(attr).value.split(', ')
            for prop in props:
                if prop not in attr_dict:
                    raise exceptions.UnsupportedAttributeError('Параметр ' + prop + ' не поддерживается.')
                else:
                    attr_dict[prop] = True


def _parse_schema(dom_schema):
    """
    Преобразовать dom-структуру, представляющу схему базы, в объект.
    :param dom_schema: dom-структура схемы.
    :return: объект схемы.
    """
    try:
        schema = Schema()
        parse_attributes(schema.attributes, dom_schema.attributes)
    except exceptions.UnsupportedAttributeError as ex:
        raise Exception('Не удалось создать схему. ' + str(ex))
    try:
        for child in dom_schema.childNodes:
            if _check_node(child):
                continue
            elif child.tagName == 'domains':
                _parse_domain(schema, child)
            elif child.tagName == 'tables':
                _parse_table(schema, child)
            elif child.tagName != 'custom':
                raise exceptions.UnsupportedTagError('Некорректно задан тэг: ' + child.tagName)
    except Exception as ex:
        raise Exception('Схема ' + schema.get('name') + ': ' + str(ex))
    _validate_schema(schema)
    return schema


def _validate_schema(schema):
    """
    Проверить корректность данных схемы (произвести валидацию)
    :param schema: объект схемы к валидации.
    :return: None
    """
    try:
        # Выполняется валидация объекта схемы.
        schema.validate()
        # Выполняется валидация каждой из таблиц схемы.
        for table in schema.tables.values():
            try:
                # Выполняется валидация каждого ограничения таблицы.
                for constraint in table.constraints:
                    try:
                        constraint.validate()
                        # Выполняется валидация деталей ограничения.
                        for detail in constraint.details:
                            try:
                                detail.validate()
                            except Exception as ex:
                                raise Exception('Деталь ограничения.' + str(ex))
                    except Exception as ex:
                        raise Exception('Ограничение.' + str(ex))
                # Выполняется валидация каждого индекса таблицы.
                for index in table.indexes:
                    try:
                        index.validate()
                        # Выполняется валидация деталей индекса.
                        for detail in index.details:
                            try:
                                detail.validate()
                            except Exception as ex:
                                raise Exception('Деталь индекса.' + str(ex))  # Производится
                    except Exception as ex:                                   # каскадный
                        raise Exception('Индекс. ' + str(ex))                 # проброс
            except Exception as ex:                                           # исключений.
                raise Exception('Таблица ' + str(table.get('name')) + '. ' + str(ex))
    except Exception as ex:
        raise Exception('Схема ' + str(schema.get('name')) + '. ' + str(ex))


def _parse_domain(schema, dom):
    """
    Преобразовать список dom-элементов, представляющих домены, в список доменов схемы.
    :param schema: схема, содержащая получаемые домены.
    :param dom: список dom-объектов доменов.
    :return: None
    """
    domains = dom.childNodes
    try:
        for domain_element in domains:
            if _check_node(domain_element):
                continue
            elif domain_element.tagName != 'domain':
                raise exceptions.UnsupportedTagError('Некорректно задан тэг: ' + domain_element.tagName)
            domain = Domain(schema)
            parse_attributes(domain.attributes, domain_element.attributes)
            domain.validate()
    except Exception as ex:
        raise Exception('Домен. ' + str(ex))


def _parse_table(schema, dom):
    """
    Проебразовать список dom-элементов, представляющих таблицы, в список таблиц схемы.
    :param schema: схема, содержащая получаемые таблицы.
    :param dom: список dom-объектов таблиц.
    :return: None
    """
    tables = dom.childNodes
    for table_element in tables:
        if _check_node(table_element):
            continue
        elif table_element.tagName != 'table':
            raise exceptions.UnsupportedTagError('Некорректно задан тэг: ' + table_element.tagName)
        table = Table(schema)
        parse_attributes(table.attributes, table_element.attributes)
        table.validate()

        try:
            for child in table_element.childNodes:
                if _check_node(child):
                    continue
                elif child.tagName == 'field':
                    field = Field(table)
                    parse_attributes(field.attributes, child.attributes)
                    field.validate()
                elif child.tagName == 'index':
                    _parse_index(table, child)
                elif child.tagName == 'constraint':
                    _parse_constraint(table, child)
                else:
                    raise exceptions.UnsupportedTagError('Некорректно задан тэг: ' + table_element.tagName)
        except Exception as ex:
            raise Exception('Таблица: ' + table.get('name') + '. ' + str(ex))


def _parse_constraint(table, constraint_element):
    """
    Преобразовать dom-объект, представляющий ограничение, в объект ограничения.
    :param table: таблица, содержащая получаемое ограничение.
    :param constraint_element: dom-объект, представляющий ограничение.
    :return: None
    """
    try:
        constraint = Constraint(table)
        parse_attributes(constraint.attributes, constraint_element.attributes)
        for item in constraint_element.getElementsByTagName('item'):
            detail = ConstraintDetail(constraint)
            parse_attributes(detail.attributes, item.attributes)
    except Exception as ex:
        raise Exception('Ограничение. ' + str(ex))


def _parse_index(table, index_element):
    """
    Преобразовать dom-объект, представляющий индекс, в объект индекса.
    :param table: таблица, содержащая получаемый индекс.
    :param index_element: dom-объект, представляющий индекс.
    :return: None
    """
    try:
        index = Index(table)
        parse_attributes(index.attributes, index_element.attributes)
        for item in index_element.getElementsByTagName('item'):
            detail = IndexDetail(index)
            parse_attributes(detail.attributes, item.attributes)
    except Exception as ex:
        raise Exception('Индекс. ' + str(ex))

