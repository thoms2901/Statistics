"""Build the English letter statistics used by hw3/index.html.

Training corpus: public-domain novels from the NLTK copy of Project Gutenberg
(Austen x3, Chesterton x3, Melville, Edgeworth). Test text: Alice in
Wonderland, kept out of training so the attack is tested on unseen text.

Run: python3 build_corpus.py > corpus.json   (needs nltk + gutenberg corpus)
"""
import json, math, re
from collections import Counter
from nltk.corpus import gutenberg

TRAIN = ["austen-emma.txt", "austen-persuasion.txt", "austen-sense.txt",
         "chesterton-ball.txt", "chesterton-brown.txt", "chesterton-thursday.txt",
         "melville-moby_dick.txt", "edgeworth-parents.txt"]
TEST = "carroll-alice.txt"

def letters(text):
    return re.sub(r"[^A-Z]", "", text.upper())

train = "".join(letters(gutenberg.raw(f)) for f in TRAIN)
uni = Counter(train)
bi = Counter(train[i:i + 2] for i in range(len(train) - 1))
tri = Counter(train[i:i + 3] for i in range(len(train) - 2))

A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N1, N2, N3 = len(train), len(train) - 1, len(train) - 2
# log10 probabilities, unseen n-grams get count 0.5 (simple floor)
big = [round(math.log10(max(bi[a + b], 0.5) / N2), 3) for a in A for b in A]
trig = [round(math.log10(max(tri[a + b + c], 0.5) / N3), 2) for a in A for b in A for c in A]

# test text: drop the Gutenberg header, keep words and spaces only
raw = gutenberg.raw(TEST)
raw = raw[raw.find("CHAPTER I"):]
test = re.sub(r"\s+", " ", re.sub(r"[^A-Za-z ]", " ", raw.replace("\n", " "))).strip().upper()

print(json.dumps({
    "trainLetters": N1,
    "trainBooks": TRAIN,
    "uni": [uni[a] for a in A],
    "bi": big,
    "tri": trig,
    "test": test[:60000],
}, separators=(",", ":")))
