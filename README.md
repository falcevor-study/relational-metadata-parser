# collective-development
Repository contains implementations of cours tasks by Daniil Lukinov.
Что реализовано:
1. Реализовано преобразование текстового представления базы в представление в RAM:
  * реализованы классы, моделирующие элементы базы (модуль structure)
  * реализован модуль, позволяющий произвести рабор текстового представления в объектное (модуль xml_reader)
  * реализованы методы валидации (проверки корректности данных) элементов объектного представления (модуль structure)
  * реализован каскадный проброс ошибок, позволяющий получить больше информации о местоположении неверно заданных элементов (модули structure, xml_reader)
  * реализованы преобразование и загрузка структурированных индексов и ограничений по средствам создания деталей (модули structure, xml_reader)
2. Реализовано преобразование объектного представления базы в текстовое:
  * реализован модуль, позволяющий произвести данное преобразование (модуль xml_writer)
3. Реализован модуль для тестового запуска реализованных процедур, который:
  * выполняет преобразование двух предоставленных тестовых файлом в объектное представление в RAM (модуль main)
  * полученные модели преобразует обратно в текстовое представление XML (модуль main)
  * производит построчную сверку файлов с точностью до межстрочных разделителей и делает заключение об идентичности (модуль main)
  
  
Что получилось в итоге:
Запуск программы был произведен на двух тестовых файлах, по результатам выполнения было получено заключение об идентичности полученного и исходного файлов.
Были внесены изменения в один из исходных файлов, заключающиеся в добавлении структурированных индексов и ограничений, следующего вида:
  
  <constraint kind="FOREIGN" reference="example_table">
    <item value="field1"/>
    .....
    <item value="fieldN"/>
  </constraint>
  
  <index prop="uniqueness">
    <item value="field1"/>
    .....
    <item value="fieldN"/>
  </index>
(данная структура была представлена на одной из лекций)

Результат - также успешное выполнение.


Как запустить:
Необходимо выполнить процедуру execute из модуля main. На вход данная процедура принимает 2 параметра - путь в файловой системе к исходнму файлу и путь к файлу, в который должна быть произведена выгрузка результата.
Результат выполнения процедура - заключение об идентичности/неидентичности файлов, либо сообщение об ошибке, если в структуре файла есть искажения.
