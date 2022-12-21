import ipadic
from fugashi import GenericTagger

WAKATI_TESTS = (
    ("すももももももももの内", "すもも も もも も もも の 内"),
    ("日本語ですよ", "日本語 です よ"),
    ("深海魚は、深海に生息する魚類の総称。", "深海魚 は 、 深海 に 生息 する 魚類 の 総称 。"),
)


def test_wakati():
    tagger = GenericTagger(ipadic.MECAB_ARGS + " -Owakati")

    for i in WAKATI_TESTS:
        b = tagger.parse(i[0])
        print(b)


test_wakati()
