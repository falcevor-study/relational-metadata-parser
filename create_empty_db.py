import sys

import db_deploy.ddl_applying as deploy

if len(sys.argv) != 2:
    raise KeyError('Ожидается 2 параметра: название БД; путь к XML или DBD представлению.')

db_name = sys.argv[0]
repr_file = sys.argv[1]

print('Создание пустой БД PostgreSQL...')
db = deploy.DbCreationConnection('database.cfg', 'dbd_queries_sqlite.cfg')
db.deploy(db_name=db_name, repr_file=repr_file)

print('Выполнение завершено.')
