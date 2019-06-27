import json

import tweepy
from tweepy import StreamListener, Stream, OAuthHandler

consumerKey = 'bnAUfQo7zPyMU5yVUW3Kzavnm'
consumerSecret = 'jLH2elGUsAXHl94Lsz7WFn9RWGXWNevhqWeZ21mYNxEwokkoM0'
accessToken = '1050068828011593728-xN14C5Smumyz9fZhKC3itPHTihX19O'
accessSecret = 'DJwPoPSsieO19nX2175sfMz44wCYlVamQlkMD5gfSNkv8'
auth = OAuthHandler(consumerKey, consumerSecret)  # oggetto autenticatore
auth.set_access_token(accessToken, accessSecret)  # token d'accesso
api = tweepy.API(auth)

#"""
# CHIEDERE AL PROF COME ANALIZZARE (FARE PRE-PROCESSING) I DATI MAN MANO CHE LI SALVO NEL JSON
# # # STREAM # # #
class MyListener(StreamListener):

    def on_data(self, data):
        with open('tweet_in_ascolto_huawei.json', 'a+') as fw:
            fw.write(data)
            return True

    def on_error(self, status_code):
        print(status_code)
        return True


myStream = tweepy.Stream(auth=api.auth, listener=MyListener,
                         wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True, tweet_mode= 'extended')  # oggetto tweet API per fetchare i tweet

print("***** RICERCA DEI TWEET  *****")
stream = Stream(auth, MyListener())
keyword = input("Che hashtag vuoi cercare: ").replace(" ", "")
#stream.filter(track=['#' + keyword + ''], languages=["en"])
stream.filter(track=['' + keyword + ''], languages=["en"])



# # # -------- # # #
#"""