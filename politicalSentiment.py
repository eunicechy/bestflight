import urllib.request
import string
from bs4 import BeautifulSoup
import plotly
import plotly.graph_objs as go
import cities
import re
import specialwords


class Ps:
    def __init__(self, city):
        self.url = cities.city_url[cities.city_name.index(city)]
        self.city = city
        self.text = ""
        self.word_list = []
        self.get_text()
        self.positive_words = []
        self.negative_words = []

        for i in range(len(self.word_list)):
            if self.word_list[i].casefold() in specialwords.positive_words:
                self.positive_words.append(self.word_list[i].casefold())
            elif self.word_list[i].casefold() in specialwords.negative_words:
                self.negative_words.append(self.word_list[i].casefold())

        self.neutral_words = [x for x in self.word_list if x not in self.negative_words and self.negative_words]
        self.neutral_words_hash = []

        for i in range(len(self.neutral_words)):
            self.neutral_words_hash.append(specialwords.hashing(self.neutral_words[i]))

        self.neutral_words_nsw = []
        self.remove_sw(self.neutral_words)

    def get_text(self):
        url = self.url
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        file = open(self.city + ".txt", "w", encoding="utf-8")
        try:
            file.write(text)
        finally:
            file.close()

        file2 = open(self.city + ".txt", "r", encoding="utf-8")
        try:
            content = file2.read()
        finally:
            file2.close()

        self.text = content
        content = content.replace('\n', ' ')

        self.word_list = [z.casefold() for z in re.sub('['+string.punctuation+']', '', content).split()]

    def remove_sw(self, alist):
        print()

    def total_words(self):
        print("number of words: " + str(len(self.word_list)))

    def word_frequency(self):
        word_dict = {}
        for i in range(len(self.word_list)):
            if str.casefold(self.word_list[i]) not in word_dict:
                word_dict[str.casefold(self.word_list[i])] = 1
            else:
                word_dict[str.casefold(self.word_list[i])] += 1
        print(word_dict)

    def get_positive_words(self):
        return len(self.positive_words)

    def get_negative_words(self):
        return len(self.negative_words)

    def get_political_score(self):
        return self.get_positive_words() - self.get_negative_words()

    def calculate_political_score(self):

        for i in range(len(self.word_list)):
            if self.word_list[i].casefold() in specialwords.positive_words:
                self.positive_words.append(self.word_list[i].casefold())
            elif self.word_list[i].casefold() in specialwords.negative_words:
                self.negative_words.append(self.word_list[i].casefold())

    def print_graph1(self):
        plotly.offline.plot({
            "data": [
                go.Histogram(
                    histfunc="sum",
                    y=[len(self.positive_words), len(self.negative_words), len(self.neutral_words)],
                    x=["positive words", "negative words", "neutral words", "neutral w/o stop words"],
                    name="sum"
                )
            ],
            "layout": go.Layout(title="Positive and Negative Word Count")
        }, auto_open=False, filename=self.city+"graph.html")

