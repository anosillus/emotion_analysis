a = {"value": "55"}
b = {"value": "50"}

aa = hash(frozenset(a.items()))
bb = hash(frozenset(b.items()))

hash_table = {aa: a, bb: b}

c = {aa: "9", bb: "14"}
print(c)

for i in c.keys():
    print(hash_table.get(i))
    print(hash_table.get(i).get("value"))
