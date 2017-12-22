import sys

import ram_repr.ram_to_dbd as ram2dbd
import xml_repr.xml_to_ram as xml2ram

if len(sys.argv) != 2:
    raise KeyError('Ожидается 2 параметра: путь к файлу с XML; путь для создания DBD.')

xml = sys.argv[0]
dbd = sys.argv[1]

print('Создания RAM представления...')
schemas = xml2ram.read(xml)

print('Создание DBD представления...')
ram2dbd.upload(schemas, dbd)

print('Выполнение завершено.')
