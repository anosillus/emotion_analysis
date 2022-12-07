import csv

# tsvファイルのパス
file_path = "./../data/wrime-ver1.tsv"

# tsvファイルを読み込む
with open(file_path, "r") as f:
    # csv.readerを使って、tsvファイルを読み込む
    reader = csv.reader(f, delimiter="\t")
    # 一行目をカラムとして取得
    columns = next(reader)

    for row in reader:
        data = dict(zip(columns, row))

        print(data)

        break
