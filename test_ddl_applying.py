from ddl_applying import DbCreationConnection

db = DbCreationConnection('database.cfg')
db.deploy('Collective', r'C:\Studying\Коллективная разработка ПО\dbd_repr.db')
db.deploy('development', r'C:\Studying\Коллективная разработка ПО\prjadm.xml')
