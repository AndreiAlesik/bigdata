#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()  # Удаление лишних пробельных символов
    fields = line.split('\u0001')  # Разбиваем строку на поля
    
    # Убедимся, что у нас достаточно полей
    if len(fields) < 12:
        continue  # Skip lines that don't have enough fields

    label_id = fields[6]
    artist_id = fields[4]
    artist_name = fields[5]
    genre = fields[8]
    release_date = fields[11]

    # Проверяем, что дата релиза имеет ожидаемый формат и вычисляем декаду
    try:
        year = int(release_date[:4])
    except ValueError:
        continue  # Skip lines with invalid release dates

    decade = (year // 10) * 10

    # Выводим ключ (label_id, artist_id, decade, genre) и значение 1
    # Используем sys.stdout.write для надежности в Hadoop Streaming
    sys.stdout.write("{}\t{}\t{}\t{}\t{}\t1\n".format(label_id, artist_id, artist_name, decade, genre))
