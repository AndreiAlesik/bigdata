#!/usr/bin/env python
import sys
from collections import defaultdict

# Словарь для подсчета количества пластинок и жанров
label_artist_decade = defaultdict(lambda: {'count': 0, 'genres': set()})

current_key = None

for line in sys.stdin:
    # Удаление лишних пробельных символов
    line = line.strip()
    # Разбиваем строку на ключ и значение
    label_id, artist_id, artist_name, decade, genre = line.split('\t')
    
    # Создаем ключ для словаря
    key = (label_id, artist_id, artist_name, decade)
    
    # Считаем количество пластинок и добавляем жанры в множество
    label_artist_decade[key]['count'] += 1
    label_artist_decade[key]['genres'].add(genre)

# Выводим результаты
for key, value in label_artist_decade.items():
    label_id, artist_id, artist_name, decade = key
    count = value['count']
    genres = list(value['genres'])
    print(f'{label_id}\t{artist_id}\t{artist_name}\t{decade}\t{count}\t{genres}')

