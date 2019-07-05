from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import csv

def display_topics(model, feature_names, no_top_words):
    print()
    for topic_idx, topic in enumerate(model.components_):
        print("* Top 10 parole prevalenti per il topic #", topic_idx + 1, "*")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        print()


def save_topics(model, feature_names, no_top_words, username):
    for topic_idx, topic in enumerate(model.components_):
        with open('tweet_topics_'+username+'.csv', 'a+') as file:
            writer = csv.writer(file)
            writer.writerow([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])


def topic_process():

    username = input("Inserisci l'username dell'utente twitter: ")
    print(username)
    try:
        miei_tweets = open('tweet_estratti_prepro_'+username+'.csv')
        no_features = 1000

        tf_vectorizer = CountVectorizer(max_df=0.80, min_df=2, max_features=no_features)
        tf = tf_vectorizer.fit_transform(miei_tweets).toarray()
        # print("(Document_ID, Token_ID) - TF-IDF del token nel documento\n", tf)

        # fetch dei termini (da indice del termine a valore del termine - Es. 1342 = dog)
        tf_feature_names = tf_vectorizer.get_feature_names()

        no_topics = 20

        # LDA
        # n_components = numero di topic che vogliamo
        # learning_method = metodo utilizzato per l'addestramento (online o batch)
        # max_iter = numero massimo di iterazioni
        # learning_offset = parametro positivo che abbassa le iterazioni iniziali nell'apprendimento online (>1)
        # random_state = seed per il generatore random di numeri
        lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,
                                        random_state=0).fit(tf)

        # 10 parole più prevalenti nel topic
        no_top_words = 10

        display_topics(lda, tf_feature_names, no_top_words)
        save_topics(lda, tf_feature_names, no_top_words, username)

    except Exception as e:
        print(e)
        print("Username inserito non esistente")
