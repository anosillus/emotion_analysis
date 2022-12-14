import pickle
import urllib.request
from pathlib import Path

stopwords_url = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
with urllib.request.urlopen(stopwords_url) as response:
    stopwords = [line.decode("utf-8").strip() for line in response if not line == ""]

print(stopwords)
