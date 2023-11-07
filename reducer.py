#!/usr/bin/env python3

import sys

current_label = None
current_artist = None
current_decade = None
current_genre_set = set()
count = 0

for line in sys.stdin:
    label_id, artist_id, artist_name, decade, genre, _ = line.strip().split("\t")
    key = (label_id, artist_id, artist_name, decade)
    
    if (current_label, current_artist, current_decade) == key[:3]:
        current_genre_set.add(genre)
        count += 1
    else:
        if current_label:
            genres_list = ','.join(current_genre_set)
            print("{}\t{}\t{}\t{}\t{}".format(current_label, current_artist, current_decade, count, genres_list))
        current_label, current_artist, current_decade = key[:3]
        current_genre_set = set([genre])
        count = 1

if current_label:
    genres_list = ','.join(current_genre_set)
    print("{}\t{}\t{}\t{}\t{}".format(current_label, current_artist, current_decade, count, genres_list))
