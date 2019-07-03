from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

with open('tweet_topics.csv', 'r+') as tweet_file:
    for tweet in tweet_file.readlines():
        print(tweet)
        with open('movie_dataset.csv', 'r+') as movie_file:
            for movie in movie_file.readlines():
                movie = movie.replace('\r\n', '')
                print(movie)

'''
# Define the documents
doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"

doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"

doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"

documents = [doc_trump, doc_election, doc_putin]

# Create the Document Term Matrix
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
sparse_matrix = count_vectorizer.fit_transform(documents)
#print(sparse_matrix)
print("\ncount_vectorizer.get_feature_names()\n", count_vectorizer.get_feature_names())
# OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
doc_term_matrix = sparse_matrix.todense()
print(doc_term_matrix)
df = pd.DataFrame(doc_term_matrix,
                  columns=count_vectorizer.get_feature_names(),
                  index=['doc_trump', 'doc_election', 'doc_putin'])

print(df)
print("\ncosine_similarity\n",cosine_similarity(df, df))
'''