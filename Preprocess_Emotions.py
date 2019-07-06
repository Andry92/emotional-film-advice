import csv
import re
import string
from time import sleep

from nltk import PorterStemmer
from nltk.corpus import stopwords


def preprocess_emotions_script():
    print()
    print("*** ESECUZIONE IN BACKGROUND >>> Preprocessing delle emozioni in corso...")
    sleep(0.2)
    # # # TOKENIZZAZIONE # # #
    emoticons_str = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

    def tokenize(s):
        return tokens_re.findall(s)

    def preprocess(s, lowercase=False):
        tokens = tokenize(s)
        # if lowercase:
        # tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    punteggiatura = list(string.punctuation)  ### La punteggiatura la teniamo in conto
    stop_words = stopwords.words('english') + punteggiatura
    ps = PorterStemmer()
    # # # ------------- # # #

    with open('text_emotion.csv', 'r') as emotion_file:
        reader = csv.reader(emotion_file, delimiter=',')
        for row in reader:
            content = row[3]
            emotion = row[1]
            # print(line)
            # print()
            content = re.sub(r"(?:\@|https?\://)\S+", "", content)
            # content = re.sub(r"http\S+", "", content)
            # print("TOKENIZZAZIONE TWEET [",i,"]")
            # print("TESTO TWEET > ", preprocess(tweet))  # stampa dei token del testo dei tweets
            # print("\n")
            # i = i + 1
            # print(content)

            # lista dei termini senza le stop words (SW)
            content_prepro = [ps.stem(term) + " " for term in preprocess(content) if term not in stop_words]

            # print(content_prepro)
            # print()
            # print(emotion)

            with open('text_emotion_prepro.csv', 'a+', encoding='utf8') as file:
                file.writelines(content_prepro)
                file.writelines(",")
                file.writelines(emotion)
                file.write("\n")
    print("*** Completato! Puoi procedere...\n")