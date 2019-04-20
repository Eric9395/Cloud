import couchdb
import tweepy
import requests
import time
def save_data(data, server, tweets_db):
    server = couchdb.Server('http://Admin:admin@127.0.0.1:5984/')
    tweets_db = server['tweets']
    doc = {'zzx': 'zixuan'}
    tweets_db.save(doc)

consumer_key = 'Zf28oOjHPsWlCgZ0n9TF42XDg'
consumer_secret = 'jnWreweMUzZwSYRlL5hAEqpGGIO8DMVMAhtRqOG7fmiTHzM3bN'
access_token = '1119421816508825600-eEehgx2JYnp8frBiNJCMrTxdEdaCps'
access_token_secret = 'u16kBCbFQwl0kCOkFGTMoM4oEmRHGuP4FBsbXp0kv3NHC'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
places = api.geo_search(query='Melbourne')
places_ids = []
for place in places:
    if place.country_code == 'AU':
        places_ids.append(place.id)

count = 0
all = []
f = open('tweet.txt','a',encoding='UTF-8')
total_count = 0
for place_id in places_ids:
    place_count = 0
    print(place_id,'\n')
    SINCE_ID = 0
    MAX_ID = SINCE_ID + 100
    tweet_id = []
    MAX_QUERIES = 100
    while(MAX_QUERIES>0):
        try:
            if SINCE_ID == 0:
                for tweet in api.search(q="place:%s" % place_id,count=100):
                    tweet_id.append(tweet.id)
                    print(tweet)
                    f.write(str(tweet._json)+'\n')
                    all.append(tweet)
                    total_count+=1
                    place_count+=1
                SINCE_ID = max(tweet_id)
                MAX_ID = SINCE_ID+100
                MAX_QUERIES -= 1
            else:
                for tweet in api.search(q="place:%s" % place_id,count=100,since_id=SINCE_ID, max_id=MAX_ID):
                    tweet_id.append(tweet.id)
                    print(tweet)
                    f.write(str(tweet._json)+'\n')
                    all.append(tweet)
                SINCE_ID = max(tweet_id)
                MAX_ID = SINCE_ID + 100
                MAX_QUERIES -= 1
        except tweepy.error.RateLimitError as e:
            print(e)
            time.sleep(60)
            continue
    print(place_count,'\n')
print(len(all))
