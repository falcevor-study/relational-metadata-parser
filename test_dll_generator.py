import re
import unittest

from ddl_generator import DdlGenerator
from ram_structure import Domain
from ram_structure import Field
from ram_structure import Schema
from ram_structure import Table


class TestDdlGenerator(unittest.TestCase):
    def setUp(self):
        self.white_space = re.compile(r"^\s+", re.MULTILINE)

        self.generator = DdlGenerator()
        self.schema = Schema()
        self.schema.name = 'dbo'

        self.domain = Domain()
        self.domain.name = 'Salary'
        self.domain.type = 'string'
        self.domain.char_length = 100
        self.domain.description = 'Зарплата работников'

        self.table = Table()
        self.table.name = 'EMPLOYEE_SALARY'
        field1 = Field()
        field1.name = 'Name'
        field1.type = 'string'
        self.table.fields['Name'] = field1
        field2 = Field()
        field2.name = 'Salary'
        field2.domain = 'Salary'
        self.table.fields['Salary'] = field2

    def test_create_schema_dll(self):
        ddl = self.generator.create_schema_dll(self.schema)
        self.assertEqual(ddl.replace('\n', ''), 'CREATE SCHEMA dbo')

    def test_create_domain_ddl(self):
        result = self.generator.create_domain_dll(self.domain, self.schema)

        ddl = '''
        CREATE DOMAIN dbo."Salary"
        AS varchar(100);

        COMMENT ON DOMAIN dbo."Salary"
        IS 'Зарплата работников';
        '''
        self.assertEqual(self.white_space.sub("", ddl).replace('\n', ''),
                         self.white_space.sub("", result).replace('\n', ''))


    def test_create_table_ddl(self):
        result = self.generator.create_table_ddl(self.table, self.schema)
        print(result)
