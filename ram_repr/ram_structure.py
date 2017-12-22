""" Модуль, содержащий реализации классов представления базы в RAM.
"""


class Schema:
    """ Класс, моделирующий схему базы.
    """
    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.description = None

        self.domains = {}
        self.tables = {}
        self.data_types = ('STRING', 'SMALLINT', 'INTEGER', 'WORD', 'BOOLEAN', 'FLOAT', 'CURRENCY', 'BCD', 'FMTBCD',
                           'DATE', 'TIME', 'DATETIME', 'TIMESTAMP', 'BYTES', 'VARBYTES', 'BLOB', 'MEMO', 'GRAPHIC',
                           'FMTMEMO', 'FIXEDCHAR', 'WIDESTRING', 'LARGEINT', 'COMP', 'ARRAY', 'FIXEDWIDECHAR',
                           'WIDEMEMO', 'CODE', 'RECORDID', 'SET', 'PERIOD', 'BYTE'
                           )


class Domain:
    """ Класс, реализующий представление домена в RAM.
    """
    def __init__(self):
        self.name = None
        self.description = None
        self.type = None
        self.align = None
        self.width = None
        self.length = None
        self.precision = None
        self.char_length = None
        self.scale = None

        self.case_sensitive = False
        self.show_null = False
        self.show_lead_nulls = False
        self.thousands_separator = False
        self.summable = False


class Table:
    """ Класс, моделирующий таблицу базы в RAM.
    """
    def __init__(self):
        self.name = None
        self.description = None
        self.temporal_mode = None
        self.means = None

        self.add = False
        self.edit = False
        self.delete = False

        self.fields = {}
        self.indexes = []
        self.constraints = []


class Field:
    """ Класс, моделирующий поле базы в RAM.
    """
    def __init__(self):
        self.name = None
        self.rname = None
        self.domain = None
        self.type = None
        self.description = None

        self.input = False
        self.edit = False
        self.show_in_grid = False
        self.show_in_details = False
        self.is_mean = False
        self.autocalculated = False
        self.required = False


class Constraint:
    """ Класс, моделирующий ограничение базы в RAM.
    """
    def __init__(self):
        self.name = None
        self.kind = None
        self.reference = None
        self.constraint = None
        self.expression = None
        self.cascading_delete = None

        self.has_value_edit = False

        self.details = []


class ConstraintDetail:
    """ Класс, моделирующий деталь ограничения базы в RAM.
    """
    def __init__(self):
        self.value = None


class Index:
    """ Класс, моделирующий представление индекса базы в RAM.
    """
    def __init__(self):
        self.name = None
        self.kind = None

        self.local = False

        self.details = []


class IndexDetail:
    """ Класс, моделирующий деталь индекса в базе.
    """
    def __init__(self):
        self.value = None
        self.expression = None
        self.descend = None
