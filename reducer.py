#!/usr/bin/env python3

import sys

current_label = None
current_artist = None
current_decade = None
current_genre_set = set()
count = 0

def emit_result(label, artist, decade, count, genres):
    genres_list = ','.join(genres)
    print("{}\t{}\t{}\t{}\t{}\t{}".format(label, artist, current_artist_name, decade, count, genres_list))

for line in sys.stdin:
    label_id, artist_id, current_artist_name, decade, genre, _ = line.strip().split("\t")
    key = (label_id, artist_id, current_artist_name, decade)
    
    if (current_label, current_artist, current_decade) == key[:3]:
        current_genre_set.add(genre)
        count += 1
    else:
        if current_label:
            emit_result(current_label, current_artist, current_decade, count, current_genre_set)
        current_label, current_artist, current_artist_name, current_decade = key
        current_genre_set = set([genre])
        count = 1

if current_label:
    emit_result(current_label, current_artist, current_decade, count, current_genre_set)
