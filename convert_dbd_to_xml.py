import sys

import dbd_repr.dbd_to_ram as dbd2ram
import ram_repr.ram_to_xml as ram2xml

if len(sys.argv) != 2:
    raise KeyError('Ожидается 2 параметра: путь к файлу с DBD; путь для создания XML.')

dbd = sys.argv[0]
xml = sys.argv[1]

print('Создания RAM представления...')
schemas = dbd2ram.load('dbd_queries_sqlite.cfg', dbd)

print('Создание XML представления...')
ram2xml.write(schemas, xml)

print('Выполнение завершено.')
