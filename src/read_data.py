import pickle


def read_data(name="10000"):
    with open(f"./../data/interim/emo_dict_{name}.pickle", "rb") as f:
        emo_dict = pickle.load(f)

    with open(f"./../data/interim/emo_hash_{name}.pickle", "rb") as f:
        hash_dict = pickle.load(f)

    with open(f"./../data/interim/emo_count_{name}.pickle", "rb") as f:
        count_dict = pickle.load(f)

    return (emo_dict, hash_dict, count_dict)
