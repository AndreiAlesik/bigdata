#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()  # Удаление лишних пробельных символов
    fields = line.split('\u0001')  # Разбиваем строку на поля
    
    # Убедимся, что у нас достаточно полей
    if len(fields) >= 12:
        label_id = fields[6]
        artist_id = fields[4]
        artist_name = fields[5]
        genre = fields[8]
        release_date = fields[11]

        # Используем обработку исключений для преобразования даты
        try:
            # Вычисляем декаду
            if release_date:
                decade = (int(release_date[:4]) // 10) * 10
            else:
                # Если дата не указана, пропускаем эту запись
                continue

            # Выводим ключ (label_id, artist_id, decade) и значение (genre)
            print(f'{label_id}\t{artist_id}\t{artist_name}\t{decade}\t{genre}')
        except ValueError:
            # Если возникла ошибка преобразования, просто пропустим эту строку
            continue
    else:
        # Если полей не достаточно, пропустим эту строку
        continue
