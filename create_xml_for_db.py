import sys

import dbd_repr.dbd_to_ram as dbd2ram
import ram_repr.ram_to_xml as ram2xml

if len(sys.argv) != 2:
    raise KeyError('Ожидается 1 параметр: путь для создания XML представления.')

xml = sys.argv[0]

print('Создание выгрузка метаданных и БД...')
schemas = dbd2ram.load(queries='dbd_queries_sqlite.cfg', db_config='database.cfg')

print('Создание XML представления метаданных...')
ram2xml.write(schemas, xml)

print('Выполнение завершено.')
