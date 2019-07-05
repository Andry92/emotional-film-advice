import numpy

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import csv
import numpy as np

def cosine_similarity_script():

    username = input("Inserisci l'username dell'utente twitter: ")

    tweet_topic = []
    try:
        with open('tweet_topics_'+username+'.csv', 'r+') as tweet_file:
            for tweet in tweet_file.readlines():
                tweet_topic.append(tweet.replace("\n", ""))

        movie_topic = []
        movie_title = []
        with open('movie_dataset_500.csv', 'r+') as movie_file:
            reader = csv.reader(movie_file, delimiter=';')
            for row in reader:
                movie_topic.append(row[2])
                movie_title.append(row[1])


        '''
        tweet_0 = "environment,iceonfir,11,keep,crisi,june,premier,find,colorado,produc"
        
        movie1 = "hit in the crotch,kicked in the crotch,punched in the crotch,sparring,superhero"
        movie2 = "desire,fighting,king,spain,trap"
        movie3 = "bare chested male bondage,crime lord,die hard scenario,two word title,undercover"
        movie4 = "agent,egg,faberge egg,general,russian"
        movie5 = "one night stand,pregnancy,slacker,unplanned pregnancy,website"
        movie6 = "hospital,leukemia,oncology,sick child,terminal illness"
        movie7 = "african american protagonist,comma in title,four word title,name in title,talk show host zzz"
        movie8 = "doctor,english,india,magistrate,mosque"
        movie9 = "age difference,school,student,teacher,writing"
        movie10 = "american,bare chested male bondage,cia,detention,interrogation"
        '''
        #documents = [tweet_0, movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10]
        documents_def = []
        all_tweetid_movie_matched = []
        all_tweettopic_movie_matched = []
        only_movie_title = []

        for i in range(1, len(tweet_topic)+1):
            documents_def = []
            documents_def.append(tweet_topic[i-1])
            for elem in movie_topic:
                documents_def.append(elem)

            #print("VALORE DI i > ", i)
            #print("DOCUMENTS3 > ", documents3)
            #print("DOCUMENTS > ", documents_def)

            count_vectorizer = CountVectorizer()
            sparse_matrix = count_vectorizer.fit_transform(documents_def)
            doc_term_matrix = sparse_matrix.todense()
            df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names())

            cos_sim = cosine_similarity(df, df)
            #print("MATRICE COSENO\n", cos_sim)


            first_column = cos_sim[:, 0]
            sort_first_column = sorted(first_column)
            print()
            print("COLONNA (TRASPOSTA) ORDINATA DELLE CORRISPONDENZE TRA IL TWEET {} E LE TRAME > ".format(i), sort_first_column)
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
                # print("\n\n\n\n\nlista film > ", lista_film)
                # print("\n\n\n\n\n")
                print("TWEET TOPIC > ", tweet_topic[i])
                print("TITOLI FILM RILEVANTE > ", lista_film)

                all_tweetid_movie_matched.append("TWEET ID: " + str(i+1) + " MOVIE TITLE: " + movie_title[indice_topic_trama[0][0]-1])
                all_tweettopic_movie_matched.append("TWEET TOPIC: " + tweet_topic[i] + " MOVIE TITLE: " + movie_title[indice_topic_trama[0][0] - 1])
                only_movie_title.append(movie_title[indice_topic_trama[0][0]-1])

        print("\n\nTWEET ID-FILM MATCHATI: ",all_tweetid_movie_matched ,"\n\n")
        print("TWEET TOPIC-FILM MATCHATI: ",all_tweettopic_movie_matched, "\n\n")
        print("FILM MATCHATI: ",only_movie_title)


    except Exception as e:
        print(e)
        print("Username inserito non esistente")