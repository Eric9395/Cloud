import couchdb
import tweepy
import time
import sys


def save_data(data):
    server = couchdb.Server('http://Admin:admin@127.0.0.1:5984/')
    tweets_db = server['tweets_new']
    tweets_db.save(data)


def deal_with_tweets(tweet, tweet_id,queries_count,user_ids):
    tweet_id.append(tweet.id)
    print(queries_count, tweet)
    user_ids.add(tweet._json['user']['id_str'])
    tweet._json['_id'] = tweet.id_str
    save_data(tweet._json)
    return tweet_id, user_ids


def get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, interested_city):
    # consumer_key = 'Zf28oOjHPsWlCgZ0n9TF42XDg'
    # consumer_secret = 'jnWreweMUzZwSYRlL5hAEqpGGIO8DMVMAhtRqOG7fmiTHzM3bN'
    # access_token = '1119421816508825600-eEehgx2JYnp8frBiNJCMrTxdEdaCps'
    # access_token_secret = 'u16kBCbFQwl0kCOkFGTMoM4oEmRHGuP4FBsbXp0kv3NHC'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    places = api.geo_search(query=interested_city)
    places_ids = []
    places_name = []
    for place in places:
        if place.country_code == 'AU' and place.full_name not in places_name:
            places_ids.append((place.full_name, place.id))
            places_name.append(place.full_name)
    user_ids = set()
    for place_id in places_ids:
        print(place_id[0],place_id[1])
        max_id = 0
        tweet_ids = []
        queries_count = 0
        while True:
            try:
                if max_id == 0:
                    count = 0
                    for tweet in api.search(q="place:%s" % place_id[1], count=100):
                        tweet_id, user_ids = deal_with_tweets(tweet, tweet_ids,queries_count,user_ids)
                        count+=1
                    max_id = min(tweet_ids)
                    print(count)
                else:
                    count = 0
                    for tweet in api.search(q="place:%s" % place_id[1], count=100, max_id=max_id-1):
                        tweet_id, user_ids = deal_with_tweets(tweet, tweet_ids,queries_count,user_ids)
                        count += 1
                    max_id = min(tweet_ids)
                    print(count)
                if count == 0:
                    break
                queries_count += 1
            except tweepy.error.RateLimitError as e:
                print(e)
                time.sleep(60)
                continue
            except couchdb.http.ResourceConflict as e:
                print(e)
                continue

    for user_id in user_ids:
        for tweet in api.user_timeline(user_id=user_id, count=100):
            print(user_id, tweet)
            save_data(tweet._json)


def main(argv):
    if len(argv) < 5:
        print('command: <consumer_key> <consumer_secret> <access_token> '
              '<access_token_secret> <interested_city> <database_name>')
        sys.exit(2)
    consumer_key = argv[0]
    consumer_secret = argv[1]
    access_token = argv[2]
    access_token_secret = argv[3]
    interested_city = argv[4]
    database_name = argv[5]
    get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, interested_city)


if __name__ == '__main__':
    main(sys.argv[1:])