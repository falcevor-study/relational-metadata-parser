from db_deploy.ddl_applying import DbCreationConnection

db = DbCreationConnection('database.cfg', 'dbd_queries_sqlite.cfg')
db.deploy(db_name='Collective', repr_file=r'C:\Studying\Коллективная разработка ПО\dbd_repr.db')
db.deploy(db_name='development',repr_file=r'C:\Studying\Коллективная разработка ПО\prjadm.xml')
