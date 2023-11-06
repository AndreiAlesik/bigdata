#!/usr/bin/env python3

import sys

for line in sys.stdin:
    values = line.strip().split("\u0001")
    if len(values) < 12:
        continue

    label_id = values[6]
    artist_id = values[4]
    artist_name = values[5]
    release_date = values[11]
    genre = values[8]

    if not artist_id or not release_date:
        continue

    try:
        year = int(release_date.split('-')[0])
    except ValueError:
        continue

    decade = year - (year % 10)

    if genre:
        print("{}\t{}\t{}\t{}\t{}\t{}".format(label_id, artist_id, artist_name, decade, 1, genre))
