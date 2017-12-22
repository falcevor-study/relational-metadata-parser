from db_deploy import ddl_applying
from dbd_repr import dbd_to_ram

schemas = dbd_to_ram.load('dbd_queries_mssql.cfg')
db = ddl_applying.DbCreationConnection('database.cfg', 'dbd_queries_mssql.cfg')
db.deploy(db_name='Northwind', schemas=schemas)