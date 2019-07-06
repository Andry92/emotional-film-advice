from time import sleep

import numpy

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import csv
import numpy as np
from textblob.classifiers import NaiveBayesClassifier


def cosine_similarity_script():
    username = input("Inserisci l'username dell'utente twitter: ")
    print("*** ELABORAZIONE IN CORSO...")
    sleep(0.2)
    try:
        tweet_topic = []
        with open('tweet_topics_' + username + '.csv', 'r+') as tweet_file:
            for tweet in tweet_file.readlines():
                tweet_topic.append(tweet.replace("\n", ""))

        movie_topic = []
        movie_title = []
        movie_genre = []
        with open('movie_dataset_500.csv', 'r+') as movie_file:
            reader = csv.reader(movie_file, delimiter=';')
            for row in reader:
                movie_topic.append(row[2])
                movie_title.append(row[1])
                movie_genre.append(row[0])

        # Definizione del classificatore
        with open('text_emotion_prepro.csv', "r") as infile:
            csv_reader = csv.reader(infile, delimiter=',')
            line_count = 0
            data = []
            for row in csv_reader:
                if line_count > 0:
                    data.append((row[0], row[1]))
                line_count += 1

        cl = NaiveBayesClassifier(data)
        # Fine definizione del classificatore

        all_tweetid_movie_matched = []
        all_tweettopic_movie_matched = []
        only_movie_title = []

        for i in range(1, len(tweet_topic) + 1):
            documents_def = []
            documents_def.append(tweet_topic[i - 1])
            for elem in movie_topic:
                documents_def.append(elem)

            # Classificazione topic per estrarre l'emozione
            emozione_tweet_topic = cl.classify(tweet_topic[i-1])


            count_vectorizer = CountVectorizer()
            sparse_matrix = count_vectorizer.fit_transform(documents_def)
            doc_term_matrix = sparse_matrix.todense()
            df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names())

            cos_sim = cosine_similarity(df, df)

            first_column = cos_sim[:, 0]
            sort_first_column = sorted(first_column)
            print()
            print("COLONNA (TRASPOSTA) ORDINATA DELLE CORRISPONDENZE TRA IL TWEET {} E LE TRAME > ".format(i),
                  sort_first_column)
            punteggio_max = sort_first_column[-2]
            if punteggio_max == 0:
                print("NESSUNA CORRISPONDENZA TROVATA!")
            else:
                print("PUNTEGGIO CORRISPONDENZA MASSIMA (esclusa quella per se stesso) > ", punteggio_max)
                indice_topic_trama = np.where(first_column == sort_first_column[-2])
                print("INDICE TRAMA PIU' RILEVANTE > ", indice_topic_trama[0])

                lista_film = []
                for j in range(0, len(indice_topic_trama[0])):
                    lista_film.append(movie_title[indice_topic_trama[0][j] - 1])

                print("TWEET TOPIC > ", tweet_topic[i - 1])
                print("EMOZIONE ESTRATTA DAL TWEET TOPIC > ", emozione_tweet_topic)
                print("TITOLI FILM RILEVANTI > ", lista_film)

                all_tweetid_movie_matched.append(
                    "TWEET ID: " + str(i + 1) + " MOVIE TITLE: " + movie_title[indice_topic_trama[0][0] - 1])
                all_tweettopic_movie_matched.append(
                    "TWEET TOPIC: " + tweet_topic[i - 1] + " MOVIE TITLE: " + movie_title[indice_topic_trama[0][0] - 1])
                only_movie_title.append(movie_title[indice_topic_trama[0][0] - 1])


        print("\n\nTWEET ID - FILM TROVATI > ", all_tweetid_movie_matched, "\n\n")
        print("TWEET TOPIC - FILM TROVATI > ", all_tweettopic_movie_matched, "\n\n")
        print("FILM TROVATI TOTALI > ", only_movie_title)


    except Exception as e:
        print(e)
        print("Username inserito non esistente")

