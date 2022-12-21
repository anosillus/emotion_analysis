import csv
import pickle
import urllib.request
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

import ipadic
import numpy as np
from tqdm import tqdm

import vibrato


def get_tokenizer():
    with open("./vibrato/ipadic-mecab-2_7_0/system.dic", "rb") as fp:
        dict_data = fp.read()

    return vibrato.Vibrato(dict_data)


# tokens = tokenizer.tokenize("社長は火星猫だ")
# print(list(tokens))

emo_file_path = "./../data/wrime-ver1.tsv"

MECAB_RESULT_INDEX = [
    "品詞",
    "品詞細分類1",
    "品詞細分類2",
    "品詞細分類3",
    "活用型",
    "活用形",
    "原形",
    "読み",
    "発音",
]


def read_stopwords() -> list[str]:

    if not Path("./../data/stopwords.pickle").exists():
        stopwords_url = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
        sub_words_url = "https://gist.githubusercontent.com/ftnext/2e14fb57c96ca276ee4d28eccfcecd96/raw/f0b1557cd576fa223cb954fc983f5117b3372ac9/stop_words.txt"
        original_words = """ない ある える くる
あ あっ あまり あり ある あるいは あれ
い いい いう いく いずれ いっ いつ いる いわ
うち
え
お おい おけ および おら おり
か かけ かつ かつて かなり から が
き きっかけ
くる くん
こ こう ここ こと この これ ご ごと
さ さらに さん
し しか しかし しまう しまっ しよう
す すぐ すべて する ず
せ せい せる
そう そこ そして その それ それぞれ
た たい ただし たち ため たら たり だ だけ だっ
ち ちゃん
つ つい つけ つつ
て で でき できる です
と とき ところ とっ とも どう
な ない なお なかっ ながら なく なけれ なし なっ など なら なり なる
に にて
ぬ
ね
の のち のみ
は はじめ ば
ひと
ぶり
へ べき
ほか ほとんど ほど ほぼ
ま ます また まで まま
み
も もう もっ もと もの
や やっ
よ よう よく よっ より よる よれ
ら らしい られ られる
る
れ れる
を
ん
一
""".split()

        with urllib.request.urlopen(stopwords_url) as response:
            stopwords = [
                line.decode("utf-8").strip()
                for line in response
                if not line in ("", " ")
            ]
        with urllib.request.urlopen(sub_words_url) as response:
            sub_stopwords = [
                line.decode("utf-8").strip()
                for line in response
                if not line in ("", " ")
            ]
        stopwords = set(stopwords + sub_stopwords + original_words)

        with open("./../data/stopwords.pickle", "wb") as f:
            pickle.dump(stopwords, f)
    else:
        with open("./../data/stopwords.pickle", "rb") as f:
            stopwords = pickle.load(f)
    return stopwords


def wakachi(text="麩菓子は、麩を主材料とした日本の菓子。"):
    stopwords = read_stopwords()

    def is_target_words(word):
        return word not in stopwords and word.feature().split(",")[0] in (
            "動詞",
            "名詞",
            "形容詞",
            "連体詞",
        )

    tokenizer = get_tokenizer()

    # tokens = tokenizer.tokenize("社長は火星猫だ")
    # text = "社長は火星猫だ"
    # print(list(tokens))
    return [
        dict(zip(MECAB_RESULT_INDEX, word.feature().split(",")))
        for word in tokenizer.tokenize(text)
        if is_target_words(word)
    ]


def read_emo_data():
    file_path = "./../data/wrime-ver1.tsv"
    data = open(file_path, mode="r", encoding="utf-8-sig")
    # length 43201
    return csv.DictReader(data, delimiter="\t")


def save_data(emo_dict, hash_dict, count_dict, name):
    emo_dict = dict(emo_dict)
    hash_dict = dict(hash_dict)
    count_dict = dict(count_dict)

    with open(f"emo_dict_{name}.pickle", "wb") as f:
        pickle.dump(emo_dict, f)
    # del emo_dict

    with open(f"emo_hash_{name}.pickle", "wb") as f:
        pickle.dump(hash_dict, f)
    # del hash_dict

    with open(f"emo_count_{name}.pickle", "wb") as f:
        pickle.dump(count_dict, f)
    # del count_dict


keys = [
    "Sentence",
    "Avg. Readers_Joy",
    "Avg. Readers_Sadness",
    "Avg. Readers_Anticipation",
    "Avg. Readers_Surprise",
    "Avg. Readers_Anger",
    "Avg. Readers_Fear",
    "Avg. Readers_Disgust",
    "Avg. Readers_Trust",
]

emo_dicts = read_emo_data()

# i = 0

word_emo_dict = defaultdict(lambda: np.zeros(8, dtype=float))
word_count_dict = defaultdict(int)
word_hash_dict = defaultdict(lambda: defaultdict(str))

emo_data_len = 43201
for i, emo_dict in enumerate(tqdm(emo_dicts, total=emo_data_len)):

    emo_data = list(map(emo_dict.get, keys))
    emos = np.array(list(map(float, emo_data[1:])))
    if not emo_data:
        continue
    try:
        word_info_list = wakachi(emo_data[0])
    except RuntimeError:
        print(emo_data)
        continue

    if not word_info_list:
        continue
    per_emos = emos / len(word_info_list)
    for word_info in word_info_list:
        word = word_info.get("原形")
        # # word_hash = hash(frozenset(word_info.items()))
        word_emo_dict[word] += per_emos
        # word_hash_dict[word_hash] = word_info
        word_count_dict[word] += 1

    if i % 1000 == 0:
        save_data(word_emo_dict, word_count_dict, word_hash_dict, str(i))

save_data(word_emo_dict, word_count_dict, word_hash_dict, str(i))
del word_emo_dict
del word_count_dict
del word_hash_dict
# word_emo_dict = defaultdict(lambda: np.zeros(8, dtype=float))
# word_count_dict = defaultdict(int)
# word_hash_dict = defaultdict(lambda: defaultdict(str))

# save_data(word_emo_dict, word_count_dict, word_hash_dict, str("end"))
