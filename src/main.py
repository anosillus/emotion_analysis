import csv
import pickle
import subprocess
from collections import defaultdict
from operator import add

import numpy as np


def run_parser(sentence):
    VIVER_RUN = "cargo run --release -p tokenize -- -i ipadic-mecab-2_7_0/system.dic -S"
    ECHO = "echo "
    PIPE = "|"
    command = ECHO + sentence + PIPE + VIVER_RUN

    return subprocess.check_output(
        command, shell=True, cwd="./vibrato", encoding="utf-8", timeout=2
    )


def grep_target_words(parse_result) -> list[str]:
    results: list[str] = []

    for line in parse_result.split("\n"):
        if line == "" or line == "EOS":
            continue

        try:
            info = line.split("\t")[1]
        except IndexError:
            continue

        if info.split(",")[0] not in ("助詞", "助動詞", "記号"):
            results.append(info.split(",")[-3])

    return results


file_path = "./../data/wrime-ver1.tsv"
d = defaultdict(lambda: np.zeros(17))

with open(file_path, "r") as f:
    reader = csv.reader(f, delimiter="\t")
    columns = next(reader)

    for row in reader:
        try:
            words = grep_target_words(
                run_parser(row[0].replace("(", "").replace(")", "").replace("|", ""))
            )
        except subprocess.CalledProcessError:
            print(row)

        except Exception:
            print(row)

            continue
        vector = np.asarray(list(map(float, row[4:12] + row[-9:-1])) + [1])

        for word in words:
            if word == "*":
                continue

            d[word] += vector


with open("vector.pickle", "wb") as handle:
    pickle.dump(dict(d), handle, protocol=pickle.HIGHEST_PROTOCOL)
