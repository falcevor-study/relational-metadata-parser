"""
Модуль, содержащий метод выгрузки объектного представления базы в RAM в файловое представление в виде XML.
"""

from minidom_fixed import *
from codecs import open as _open


def _collect_attributes(db_elem, dom_elem):
    """
    Собрать аттрибуты объекта в dom-элемент.
    :param db_elem: объект базы.
    :param dom_elem: dom-объект, представляющий элемент базы.
    :return: None
    """
    props_included = False
    for attr in db_elem.attributes:
        value = db_elem.attributes[attr]
        if value is True and not props_included:
            dom_elem.setAttribute('props', str(_collect_props(db_elem)))
            props_included = True
        elif value is not None and value is not False and value is not True:
            dom_elem.setAttribute(attr, str(value))


def _collect_props(db_elem):
    """
    Собрать параметры-флаги для объекта базы в строку с разделителем.
    :param db_elem: элемент базы, представленный в RAM.
    :return: None
    """
    props = [str(attr) for attr in db_elem.attributes if db_elem.get(attr) is True]
    return ', '.join(props)


def write(schema, output):
    """
    Выгрузить структуру базы из RAM в XML-файл.
    :param schema: выгружаемая схема базы.
    :param output: путь к файлу, в который необходимо произвести выгрузку.
    :return: None
    """
    # Инициализируетс dom-структура.
    doc = Document()
    # Заполняется объект схемы.
    dbd_schema = doc.createElement('dbd_schema')
    _collect_attributes(schema, dbd_schema)
    # Заполнаяется непонятный тэг. Необходим для того, чтобы результаты сошлись в любом случае.
    custom_output = doc.createElement('custom')
    dbd_schema.appendChild(custom_output)
    # Заполняется структура доменов.
    domains_output = doc.createElement('domains')
    for domain in schema.domains.values():
        domain_output = doc.createElement("domain")
        _collect_attributes(domain, domain_output)
        domains_output.appendChild(domain_output)
    dbd_schema.appendChild(domains_output)
    # Заполняется структура таблиц.
    tables_output = doc.createElement('tables')
    for table in schema.tables.values():
        table_output = doc.createElement("table")
        _collect_attributes(table, table_output)
        for field in table.fields.values():
            # Заполняется структура поля.
            field_output = doc.createElement('field')
            _collect_attributes(field, field_output)
            table_output.appendChild(field_output)

        for constraint in table.constraints:
            # Заполняется структура ограничения.
            constraint_output = doc.createElement('constraint')
            _collect_attributes(constraint, constraint_output)
            for detail in constraint.details:
                # Заполняется структура деталей ограничений.
                detail_output = doc.createElement('item')
                _collect_attributes(detail, detail_output)
                constraint_output.appendChild(detail_output)
            table_output.appendChild(constraint_output)
        # Заполняется структура индексов.
        for index in table.indexes:
            index_output = doc.createElement('index')
            _collect_attributes(index, index_output)
            for detail in index.details:
                # Заполняется структура деталей индексов.
                detail_output = doc.createElement('item')
                _collect_attributes(detail, detail_output)
                index_output.appendChild(detail_output)
            table_output.appendChild(index_output)
        tables_output.appendChild(table_output)
    dbd_schema.appendChild(tables_output)
    doc.appendChild(dbd_schema)
    # Происходит выгрузка созданной dom-схемы в файл.
    doc.writexml(_open(output, 'w', 'utf-8'), '', '  ', '\n', 'utf-8')