"""
Модуль, содержащий метод выгрузки объектного представления базы в RAM в файловое представление в виде XML.
"""

from codecs import open as _open

from minidom_fixed import Document
from ram_structure import Constraint
from ram_structure import ConstraintDetail
from ram_structure import Domain
from ram_structure import Field
from ram_structure import Index
from ram_structure import IndexDetail
from ram_structure import Schema
from ram_structure import Table


def write(schema, output):
    """ Выгрузить структуру базы из RAM в XML-файл.

    :param schema: выгружаемая схема базы.
    :param output: путь к файлу, в который необходимо произвести выгрузку.
    :return: None
    """
    # Инициализируется dom-документ.
    doc = Document()

    # Заполняется объект схемы.
    dbd_schema = _create_schema_dom(schema, doc)
    doc.appendChild(dbd_schema)

    # Заполнаяется непонятный тэг. Необходим для того, чтобы результаты сошлись в любом случае.
    custom_output = doc.createElement('custom')
    dbd_schema.appendChild(custom_output)

    # Заполняется структура доменов.
    domains_output = doc.createElement('domains')
    dbd_schema.appendChild(domains_output)
    for domain in schema.domains.values():
        domain_output = _create_domain_dom(domain, doc)
        domains_output.appendChild(domain_output)

    # Заполняется структура таблиц.
    tables_output = doc.createElement('tables')
    dbd_schema.appendChild(tables_output)
    for table in schema.tables.values():
        table_output = _create_table_dom(table, doc)

        for field in table.fields.values():
            # Заполняется структура поля.
            field_output = _create_field_dom(field, doc)
            table_output.appendChild(field_output)

        for constraint in table.constraints:
            # Заполняется структура ограничения.
            constraint_output = _create_constraint_dom(constraint, doc)
            table_output.appendChild(constraint_output)
            if len(constraint.details) < 2:
                continue
            for detail in constraint.details:
                # Заполняется структура деталей ограничений.
                detail_output = _create_constraint_detail_dom(detail, doc)
                constraint_output.appendChild(detail_output)

        # Заполняется структура индексов.
        for index in table.indexes:
            index_output = _create_index_dom(index, doc)
            table_output.appendChild(index_output)
            if len(index.details) < 2:
                continue
            for detail in index.details:
                # Заполняется структура деталей индексов.
                detail_output = _create_index_detail_dom(detail, doc)
                index_output.appendChild(detail_output)

        tables_output.appendChild(table_output)
    # Происходит выгрузка созданной dom-схемы в файл.
    doc.writexml(_open(output, 'w', 'utf-8'), '', '  ', '\n', 'utf-8')


def _create_schema_dom(schema: Schema, doc: Document):
    """ Создать DOM-элемент Схемы, определить все его атрибуты.

    :param schema: Объект RAM-представления Схемы.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Схемы.
    """
    schema_dom = doc.createElement('dbd_schema')
    if schema.fulltext_engine:
        schema_dom.setAttribute('fulltext_engine', schema.fulltext_engine)
    if schema.version:
        schema_dom.setAttribute('version', schema.version)
    if schema.name:
        schema_dom.setAttribute('name', schema.name)
    if schema.description:
        schema_dom.setAttribute('description', schema.description)
    return schema_dom


def _create_domain_dom(domain: Domain, doc: Document):
    """ Создать DOM-элемент Домена, определить все его атрибуты.

    :param domain: Объект RAM-представления Домена.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Домена.
    """
    domain_dom = doc.createElement('domain')
    if domain.name:
        domain_dom.setAttribute('name', domain.name)
    if domain.description:
        domain_dom.setAttribute('description', domain.description)
    if domain.type:
        domain_dom.setAttribute('type', domain.type)
    if domain.align:
        domain_dom.setAttribute('align', domain.align)
    if domain.width:
        domain_dom.setAttribute('width', domain.width)
    if domain.length:
        domain_dom.setAttribute('length', domain.length)
    if domain.precision:
        domain_dom.setAttribute('precision', domain.precision)

    props = []
    if domain.case_sensitive:
        props.append('case_sensitive')
    if domain.show_null:
        props.append('show_null')
    if domain.show_lead_nulls:
        props.append('show_lead_nulls')
    if domain.thousands_separator:
        props.append('thousands_separator')
    if domain.summable:
        props.append('summable')
    if len(props) > 0:
        domain_dom.setAttribute('props', ', '.join(props))

    if domain.scale:
        domain_dom.setAttribute('scale', domain.scale)
    if domain.char_length:
        domain_dom.setAttribute('char_length', domain.char_length)
    return domain_dom


def _create_table_dom(table: Table, doc: Document):
    """ Создать DOM-элемент Таблицы, определить все его атрибуты.

    :param table: Объект RAM-представления Таблицы.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Таблицы.
    """
    table_dom = doc.createElement('table')
    if table.name:
        table_dom.setAttribute('name', table.name)
    if table.description:
        table_dom.setAttribute('description', table.description)

    props = []
    if table.add:
        props.append('add')
    if table.edit:
        props.append('edit')
    if table.delete:
        props.append('delete')
    if len(props) > 0:
        table_dom.setAttribute('props', ', '.join(props))
    return table_dom


def _create_field_dom(field: Field, doc: Document):
    """ Создать DOM-элемент Поля, определить все его атрибуты.

    :param field: Объект RAM-представления Поля.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Поля.
    """
    field_dom = doc.createElement('field')
    if field.name:
        field_dom.setAttribute('name', field.name)
    if field.rname:
        field_dom.setAttribute('rname', field.rname)
    if field.domain:
        field_dom.setAttribute('domain', field.domain)
    if field.type:
        field_dom.setAttribute('type', field.type)
    if field.description:
        field_dom.setAttribute('description', field.description)

    props = []
    if field.input:
        props.append('input')
    if field.edit:
        props.append('edit')
    if field.show_in_grid:
        props.append('show_in_grid')
    if field.show_in_details:
        props.append('show_in_details')
    if field.is_mean:
        props.append('is_mean')
    if field.autocalculated:
        props.append('autocalculated')
    if field.required:
        props.append('required')
    if len(props) > 0:
        field_dom.setAttribute('props', ', '.join(props))
    return field_dom


def _create_constraint_dom(constraint: Constraint, doc: Document):
    """ Создать DOM-элемент Ограничения, определить все его атрибуты.

    :param constraint: Объект RAM-представления Ограничения.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Ограничения.
    """
    constraint_dom = doc.createElement('constraint')
    if constraint.name:
        constraint_dom.setAttribute('name', constraint.name)
    if constraint.kind:
        constraint_dom.setAttribute('kind', constraint.kind)
    if len(constraint.details) == 1:
        constraint_dom.setAttribute('items', constraint.details[0].value)
    if constraint.reference:
        constraint_dom.setAttribute('reference', constraint.reference)
    if constraint.constraint:
        constraint_dom.setAttribute('constraint', constraint.constraint)
    if constraint.expression:
        constraint_dom.setAttribute('expression', constraint.expression)

    props = []
    if constraint.has_value_edit:
        props.append('has_value_edit')
    if constraint.cascading_delete == False:
        props.append('cascading_delete')
    if constraint.cascading_delete == True:
        props.append('full_cascading_delete')
    if len(props) > 0:
        constraint_dom.setAttribute('props', ', '.join(props))
    return constraint_dom


def _create_index_dom(index: Index, doc: Document):
    """ Создать DOM-элемент Индекса, определить все его атрибуты.

    :param index: Объект RAM-представления Индекса.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Индекса.
    """
    index_dom = doc.createElement('index')
    if index.name:
        index_dom.setAttribute('name', index.name)
    if len(index.details) == 1:
        index_dom.setAttribute('field', index.details[0].value)

    props = []
    if index.local:
        props.append('local')
    if index.kind == 'uniqueness':
        props.append('uniqueness')
    if index.kind == 'fulltext':
        props.append('fulltext')
    if len(props) > 0:
        index_dom.setAttribute('props', ', '.join(props))
    return index_dom


def _create_constraint_detail_dom(detail: ConstraintDetail, doc: Document):
    """ Создать DOM-элемент Детали ограничения, определить все его атрибуты.

    :param detail: Объект RAM-представления Детали ограничения.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Детали ограничения.
    """
    detail_dom = doc.createElement('item')
    if detail.value:
        detail_dom.setAttribute('value', detail.value)
    return detail_dom


def _create_index_detail_dom(detail: IndexDetail, doc: Document):
    """ Создать DOM-элемент Детали индекса, определить все его атрибуты.

    :param detail: Объект RAM-представления Детали индекса.
    :param doc: DOM-документ, для которого производится создание элемента.
    :return: DOM-элемент Детали индекса.
    """
    detail_dom = doc.createElement('item')
    if detail.value:
        detail_dom.setAttribute('value', detail.value)
    if detail.expression:
        detail_dom.setAttribute('expression', detail.expression)
    if detail.descend:
        detail_dom.setAttribute('descend', detail.descend)
    return detail_dom
