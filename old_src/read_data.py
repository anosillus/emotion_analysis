import subprocess

# mecabを実行するコマンド
# command = "echo 今日はいい天気ですね | mecab"
base_command = "cargo run --release -p tokenize -- -i ipadic-mecab-2_7_0/system.dic -S"
# trial = "今日はとてもよい天気ですね"
trial = "昨日はとても走って疲れた。"
# trial = "hello world"
echo = "echo "
pipe = "|"
command = echo + trial + pipe + base_command

# コマンドを実行して、結果を取得
result = subprocess.check_output(command, shell=True, cwd="./vibrato", encoding="utf-8")

def grep_target_words(parse_result):
    results = []

    for line in parse_result.split("\n"):
        if line == "" or line == "EOS":
            continue

        surface, info = line.split("\t")

        if info.split(",")[0] not in ("助詞", "助動詞", "記号"):
            results.append(info.split(",")[-3]))
