import json
import operator
from nltk import bigrams
from nltk.corpus import stopwords
import string
import re
from collections import Counter
import textblob
import matplotlib.pyplot as plot
from collections import defaultdict
import pandas





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
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


# # # ------------- # # #


# # # PRE-PROCESSING DEL TESTO CON STAMPA DEI TOKEN # # #
i = 1
with open('tweet_in_ascolto_huawei.json', 'r') as fr:
    cont_term_hash = Counter()
    cont_term = Counter()
    cont_hash = Counter()
    cont_bigram = Counter()
    cont_device_apple = Counter()
    cont_device_android = Counter()
    apple_device = 0
    android_device = 0

    # SENTIMENT
    positivo = 0
    negativo = 0
    neutrale = 0
    #polarity = 0

    for line in fr.readlines():
        tweet = json.loads(line)
        username = tweet['user']['screen_name']


        # PARTE DEL SENTIMENT
        myAnalysis = textblob.TextBlob(tweet['text'])
        #polarity += myAnalysis.sentiment.polarity
        if myAnalysis.sentiment.polarity == 0:
            neutrale += 1
        elif myAnalysis.sentiment.polarity > 0:
            positivo += 1
        elif myAnalysis.sentiment.polarity < 0:
            negativo += 1
        # ----------------------

        # STOP WORDS + PUNTEGGIATURA + ALTRO
        # lista dei termini
        lista_termini = [term for term in preprocess(tweet["text"])]


        punteggiatura = list(string.punctuation)
        stop_words = stopwords.words('english') + punteggiatura + ['rt', 'RT', 'via', '…']

        #"""
        # TERM FREQUENCY
        # lista dei termini senza le stop words (SW)
        lista_termini_SW = [term for term in preprocess(tweet["text"]) if term not in stop_words]

        # Senza duplicati
        lista_termini_SW_singola = set(lista_termini_SW)
        cont_term_hash.update(lista_termini_SW_singola)
        #"""
        # lista dei termini con solo hashtag
        term_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
        cont_hash.update(term_hash)

        # lista dei termini senza hastag o menzioni
        term_only = [term for term in preprocess(tweet['text']) if term not in stop_words and not term.startswith(('#', '@'))]
        cont_term.update(term_only)
        #"""
        # calcolo dei bigrammi solo sui termini, senza hashtag o menzioni
        term_bigrammi = bigrams(term_only)
        cont_bigram.update(term_bigrammi)
        #"""

        """
        # MATRICE DI CO-OCCORRENZA
        matrice_co = defaultdict(lambda : defaultdict(int))

        #term_only = [term for term in preprocess(tweet['text']) if term not in stop_words and not term.startswith(('#', '@'))]

        # Costruzione della matrice di co-occorrenza (matrice_co) / partire da x+1 permette di non ottenere valori del tipo
        # matrice_co[A][B] == matrice_co [B][A] / sorted mantiene i termini ordinati alfabeticamente
        for x in range(len(term_only)-1):
            for y in range(x+1, len(term_only)):
                w1, w2 = sorted([term_only[x], term_only[y]])
                if w1 != w2:
                    matrice_co[w1][w2] += 1

        # Per ogni termine, estraggo i 5 termini che co-occorrono più di frequente e li metto in una lista di tuple del tipo
        # ((termine 1, termine 2), cont)
        matrice_co_max = []
        # Per ogni termine cerchiamo la co-occorrenza più frequente comune
        for term1 in matrice_co:
            term1_max = sorted(matrice_co[term1].items(), key=operator.itemgetter(1), reverse=True)[:5]
            for term2, term2_cont in term1_max:
                matrice_co_max.append(((term1, term2), term2_cont))
        # Prendiamo le co-occorrenze più frequenti
        term_co_max = sorted(matrice_co_max, key=operator.itemgetter(1), reverse=True)
        """


        for term in tokenize((tweet['source'])):
            if term.lower() in ('iphone'):
                apple_device += 1
            elif term.lower() in ('android'):
                android_device += 1


        #print(tokenize(tweet['source']))
        #print(json.dumps(tweet, indent=4))     #stampa del json indentato
        print("TOKENIZZAZIONE TWEET [",i,"]")
        print("UTENTE >  @" + username)
        print("TESTO TWEET > ", preprocess(tweet["text"]))  # stampa dei token del testo dei tweets
        print("\n")

        i = i + 1


    print("Tweet provenienti da iPhone: ", apple_device)
    print("Tweet provenienti da Android: ", android_device)
    print()

    print("***** TERMINI PIU' COMUNI NEI TWEET ANALIZZATI ('termine', 'frequenza') *****")


    top = int(input("Quanti termini più frequenti vuoi vedere: "))
    # stampa dei primi 'top' termini più comuni nei tweet analizzati
    #print(">>> ('TERMINE', 'FREQ') <<<")
    #print(cont_term_hash.most_common(top))
    #print()
    # stampa dei primi 'top' termini più comuni nei tweet analizzati
    print(">>> ('HASHTAG', 'FREQ') <<<")
    print(cont_hash.most_common(top))
    print()
    # stampa dei primi 'top' termini più comuni nei tweet analizzati
    print(">>> ('TERMINE', 'FREQ') SENZA HASHTAG (#) O MENZIONI (@) <<<")
    print(cont_term.most_common(top))
    print()
    # stampa dei primi 'top' termini più comuni nei tweet analizzati
    #print(">>> ('BIGRAMMA', 'FREQ') SENZA HASHTAG (#) O MENZIONI (@) <<<")
    #print(cont_bigram.most_common(top))

    # Stampa della matrice di co-occorrenza
    #print("MATRICE DELLE CO-OCCORRENZE PIU' FREQUENTI DEI PRIMI 5 TERMINI\n", term_co_max[:5])




    def calcolaPercentuale(a, b):
        return 100 * float(a) / float(b)

    # i = numero tweet
    positivo = calcolaPercentuale(positivo, i)
    negativo = calcolaPercentuale(negativo, i)
    neutrale = calcolaPercentuale(neutrale, i)

    positivo = format(positivo, '.2f')
    negativo = format(negativo, '.2f')
    neutrale = format(neutrale, '.2f')




    # STAMPA PLOT
    labels = ['Positivo ', 'Neutrale', 'Negativo']
    sizes = [positivo, neutrale, negativo]
    colors = ['yellowgreen', 'gold', 'lightcoral']
    #explode = (0.1, 0, 0)
    plot.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    #plot.legend(patches, labels, loc="best")
    #plot.title('Come reagisce la gente a Game of Thrones analizzando ' + str(i) + ' tweets.\n\n')
    plot.title('Come reagisce la gente a Huawei analizzando ' + str(i) + ' tweets.\n\n')
    plot.axis('equal')
    plot.tight_layout()
    plot.show()


