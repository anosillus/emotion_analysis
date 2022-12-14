"""

"""

import csv

file_path = "./../data/wrime-ver1.tsv"
tsv = csv.DictReader(open(file_path), delimiter="\t")

keys = [
    "Avg. Readers_Joy",
    "Avg. Readers_Sadness",
    "Avg. Readers_Anticipation",
    "Avg. Readers_Surprise",
    "Avg. Readers_Anger",
    "Avg. Readers_Fear",
    "Avg. Readers_Disgust",
    "Avg. Readers_Trust",
]

for row in tsv:
    print(list(map(row.get, keys)))
