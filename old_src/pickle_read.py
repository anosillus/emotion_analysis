import pickle

with open("vector.pickle", "rb") as handle:
    unserialized_data = pickle.load(handle)
print(unserialized_data)
