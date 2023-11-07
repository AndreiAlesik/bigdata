#!/usr/bin/env python3
import sys
from collections import defaultdict

# Словарь для подсчета количества пластинок и жанров
label_artist_decade = defaultdict(lambda: {'count': 0, 'genres': set()})

for line in sys.stdin:
    line = line.strip()  # Удаление лишних пробельных символов
    # Разбиваем строку на ключ и значение
    label_id, artist_id, artist_name, decade, genre, count = line.split('\t')
    
    # Приводим count к целому числу
    count = int(count)

    # Создаем ключ для словаря
    key = (label_id, artist_id, artist_name, decade)
    
    # Считаем количество пластинок и добавляем жанры в множество
    label_artist_decade[key]['count'] += count
    label_artist_decade[key]['genres'].add(genre)

# Выводим результаты
for key, value in label_artist_decade.items():
    label_id, artist_id, artist_name, decade = key
    count = value['count']
    genres = list(value['genres'])
    # Форматируем вывод жанров как строку, разделенную запятыми
    genres_str = ','.join(genres)
    output = "{}\t{}\t{}\t{}\t{}\t{}\n".format(label_id, artist_id, artist_name, decade, count, genres_str)
    sys.stdout.write(output)
