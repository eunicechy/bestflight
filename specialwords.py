import re

file = open("positive words.txt", "r")
content = file.read()
positive_words = content.split(",")
for i in range(len(positive_words)):
    word = positive_words.pop(0)
    positive_words.append(word.strip().casefold())

file2 = open("negative words.txt", "r")
content2 = file2.read()
negative_words = content2.split(",")
for i in range(len(negative_words)):
    word = negative_words.pop(0)
    negative_words.append(word.strip().casefold())

file3 = open("stop words.txt", "r")
content3 = file3.read()
stop_words = re.sub("\n", ' ', content3).split()
for i in range(len(negative_words)):
    word = stop_words.pop(0)
    stop_words.append(word.strip().casefold())


def hashing(stop_word):
    hashval = 0
    for j in range(len(stop_word)):
        hashval += ord(stop_word[j])
    return hashval

stop_words_hash = []
for i in range(len(stop_words)):
    stop_words_hash.append(hashing(stop_words[i]))
