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
        print(row[3])
        data = dict(zip(columns, row))
        print(data)
        print(row[4:12] + row[-9:-1] + [1])
        print(len(row[4:12] + row[-9:-1] + [1]))

        # print()
        # 4data.get("Writer_Joy")
        # 5data.get("Writer_Sadness")
        # 6data.get("Writer_Anticipation")
        # 7data.get("Writer_Surprise")
        # 8data.get("Writer_Anger")
        # 9ata.get("Writer_Fear")
        # 10ata.get("Writer_Disgust")
        # 11data.get("Writer_Trust")

        # data.get("Avg. Readers_Joy")
        # data.get("Avg. Readers_Sadness")
        # data.get("Avg. Readers_Anticipation")
        # data.get("Avg. Readers_Surprise")
        # data.get("Avg. Readers_Anger")
        # data.get("Avg. Readers_Fear")
        # data.get("Avg. Readers_Disgust")
        # data.get("Avg. Readers_Trust")

        break
