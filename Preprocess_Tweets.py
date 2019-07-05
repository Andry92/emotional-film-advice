import string

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

def preprocess_tweets():

    username = input("Inserisci l'username dell'utente twitter: ")

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
        #if lowercase:
            #tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    punteggiatura = list(string.punctuation) ### La punteggiatura la teniamo in conto
    stop_words = stopwords.words('english') + punteggiatura
    ps = PorterStemmer()
    # # # ------------- # # #


    # # # PRE-PROCESSING   # # #
    i = 1
    try:
        with open('tweet_estratti_'+username+'.csv', 'r') as csv_file:
            for line in csv_file.readlines():
                tweet = line
                #print(line)
                #print()
                tweet = re.sub(r"http\S+", "", tweet)
                #print("TOKENIZZAZIONE TWEET [",i,"]")
                #print("TESTO TWEET > ", preprocess(tweet))  # stampa dei token del testo dei tweets
                #print("\n")
                i = i + 1

                # lista dei termini senza le stop words (SW)
                tweet_prepro = [ps.stem(term) + " " for term in preprocess(tweet) if term not in stop_words]

                print(tweet_prepro)
                print()

                with open('tweet_estratti_prepro_'+username+'.csv', 'a+', encoding='utf8') as file:
                    file.writelines(tweet_prepro)
                    file.write("\n")
    except Exception as e:
        print(e)
        print("Username inserito non esistente")


