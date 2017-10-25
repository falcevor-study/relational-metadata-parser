"""
Модуль, реализующий последовательный запуск создания представления базы в RAM и выгрузки данного представления назад
в XML. При этом производится сверка результата выгрузки с исходным файлом.
"""

from xml_reader import read
from xml_writer import write
from codecs import open as _open


def compare(source, result):
    """
    Построчно сравнить файлы, игнорируя незначащие отступы.
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
    """
    Запустить созадние объектного представления базы и его выгрузку в файл с последующим сравнением.
    :param input: исходный файл с представлением базы в XML.
    :param output: путь к файлу, в который необходимо произвести выгрузку.
    :return: None
    """
    schemas = read(input)
    for schema in schemas:
        write(schema, output)
    if compare(input, output):
        print('Файлы успешно прошли проверку на идентичность.')
    else:
        print('Файлы не прошли проверку на идентичность.')


execute('C:\\Studying\\Коллективная разработка ПО\\tasks.xml',
        'C:\\Studying\\Коллективная разработка ПО\\tasks1.xml')

execute('C:\\Studying\\Коллективная разработка ПО\\prjadm.xml',
        'C:\\Studying\\Коллективная разработка ПО\\prjadm1.xml')
