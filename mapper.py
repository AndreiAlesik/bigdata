#!/usr/bin/env python
import sys

for line in sys.stdin:
    # Удаление лишних пробельных символов
    line = line.strip()
    # Разбиваем строку на поля
    fields = line.split('\u0001')
    
    # Извлекаем необходимые поля
    label_id = fields[6]
    artist_id = fields[4]
    artist_name = fields[5]
    genre = fields[8]
    release_date = fields[11]
    
    # Вычисляем декаду
    decade = None
    if release_date:
        decade = (int(release_date[:4]) // 10) * 10
    
    # Выводим ключ (label_id, artist_id, decade) и значение (genre)
    if label_id and artist_id and decade:
        print(f'{label_id}\t{artist_id}\t{artist_name}\t{decade}\t{genre}')
