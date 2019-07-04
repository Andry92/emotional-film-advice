from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import csv
import numpy as np
from pprint import pprint

movie_topic = []
tweet_topic = []

with open('tweet_topics.csv', 'r+') as tweet_file:
    for tweet in tweet_file.readlines():
        tweet_topic.append(tweet.replace("\n", ""))
        with open('movie_dataset.csv', 'r+') as movie_file:
            reader = csv.reader(movie_file, delimiter=';')
            for row in reader:
                movie_topic.append(row[2])

#print("".join(tweet_topic))
list_all = []

for i in range(0,len(tweet_topic)):
    print(i)
    print(tweet_topic[i])
    documents = tweet_topic[i], movie_topic

    documents = [tweet_topic[i]]
    for elem in movie_topic:
        documents.append(elem)

    #pprint(documents)
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(documents)
    pprint(sparse_matrix)
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,
                      columns=count_vectorizer.get_feature_names(),
                      index=[])
pprint(df)

# Define the documents
'''
doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"

doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"

doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"

documents = [doc_trump, doc_election, doc_putin]
'''

'''
# Create the Document Term Matrix
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
sparse_matrix = count_vectorizer.fit_transform(documents)
#print(sparse_matrix)
print("\ncount_vectorizer.get_feature_names()\n", count_vectorizer.get_feature_names())
# OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
print("\n\nAAAAAA\n\n", count_vectorizer)
doc_term_matrix = sparse_matrix.todense()
print(doc_term_matrix)
df = pd.DataFrame(doc_term_matrix,
                  columns=count_vectorizer.get_feature_names(),
                  index=['doc_trump', 'doc_election', 'doc_putin'])

print(df)
#print("\ncosine_similarity\n",cosine_similarity(df, df))
cos_sim = cosine_similarity(df, df)
print(cos_sim)

first_column = cos_sim[:,0]
print(first_column)
sort_first_column = sorted(first_column)
print(sort_first_column[-2])
ciao = np.where(sort_first_column == sort_first_column[-2])
print("\n\nciaoooooo",ciao[0])


#print("\n",np.amax(cos_sim))
#print("\n",cos_sim.max(axis=0)[0])
'''