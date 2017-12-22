""" Тестовый модуль, реализующий последовательный запуск создания представления базы в RAM, создания DBD-представления,
а так же обратный процесс выгрузки DBD-RAM-XML. При этом производится сверка результата выгрузки с исходным файлом.
"""

from codecs import open as _open

from dbd_repr.dbd_to_ram import load
from ram_repr.ram_to_dbd import upload
from ram_repr.ram_to_xml import write
from xml_repr.xml_to_ram import read


def compare(source, result):
    """ Построчно сравнить файлы, игнорируя незначащие отступы.

    :param source: путь к исходному файлу.
    :param result: путь к результирующему файлу.
    :return: признак равенства файлов.
    """
    with _open(result, 'r', 'utf8') as source_file, \
            _open(source, 'r', 'utf8') as result_file:
        equal = True
        for source_line in source_file:
            result_line = result_file.readline()
            if source_line.split() != result_line.split():
                print('Расхождение:')
                print(source_line)
                print(result_line)
                equal = False
        return equal


def execute(input, output):
    """ Запустить созадние объектного представления базы и его выгрузку в файл с последующим сравнением.

    :param input: исходный файл с представлением базы в XML.
    :param output: путь к файлу, в который необходимо произвести выгрузку.
    :return: None
    """
    schemas = read(input)
    upload(schemas, r'C:\Studying\Коллективная разработка ПО\dbd_repr.db')
    new_schemas = load('dbd_queries_sqlite.cfg', r'C:\Studying\Коллективная разработка ПО\dbd_repr.db')

    for schema in new_schemas:
        write(schema, output)
    if compare(input, output):
        print('Файлы успешно прошли проверку на идентичность.')
    else:
        print('Файлы не прошли проверку на идентичность.')

execute('C:\\Studying\\Коллективная разработка ПО\\tasks.xml',
        'C:\\Studying\\Коллективная разработка ПО\\tasks1.xml')

execute('C:\\Studying\\Коллективная разработка ПО\\prjadm.xml',
        'C:\\Studying\\Коллективная разработка ПО\\prjadm1.xml')
