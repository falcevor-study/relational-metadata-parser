class UnsupportedTagError(Exception):
    """
    Исключение, выбрасываемое в случае некорректной структуры XML.
    """
    pass


class UnsupportedDataTypeError(Exception):
    """
    Исключение, выбрасываемое в случае, когда задан предварительно не определенный тип данных.
    """
    pass


class UnsupportedAttributeError(Exception):
    """
    Исключение, выбрасываемое в случае наличия элемента с заранее не определенным аттрибутом.
    """
    pass


class EmptyRequiredPropertyError(Exception):
    """
    Исключение, выбрасываемое в случае отсутствия обязательного к заполнению аттрибута.
    """
    pass


class UniqueViolationError(Exception):
    """
    Исключение, выбрасываемое в случае, если в структуре базы нарушается уникальность элементов.
    """
    pass


class ReferenceError(Exception):
    """
    Исключение, выбрасываемое в случае ошибочной адресации в структуре базы.
    """
    pass