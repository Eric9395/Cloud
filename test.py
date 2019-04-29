import couchdb
import tweepy
import time
import sys


def initial_database(database_name):
    global server, tweets_db
    server = couchdb.Server('http://Admin:admin@127.0.0.1:5984/')
    try:
        tweets_db = server[database_name]
    except couchdb.http.ResourceNotFound as e:
        server.create(database_name)
        tweets_db = server[database_name]


def get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, interested_city):
    total_count = 0
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
            break
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
                        tweet_ids.append(tweet.id)
                        user_ids.add(str(tweet._json['user']['id']))
                        tweet._json['_id'] = str(tweet.id)
                        try:
                            tweets_db.save(tweet._json)
                        except couchdb.http.ResourceConflict as e:
                            print(e)
                            continue
                        count += 1
                    max_id = min(tweet_ids)
                    total_count += count
                    print('Total count:', total_count, 'Query num:', queries_count, count)
                else:
                    count = 0
                    for tweet in api.search(q="place:%s" % place_id[1], count=100, max_id=max_id-1):
                        tweet_ids.append(tweet.id)
                        user_ids.add(str(tweet._json['user']['id']))
                        tweet._json['_id'] = str(tweet.id)
                        try:
                            tweets_db.save(tweet._json)
                        except couchdb.http.ResourceConflict as e:
                            print(e)
                            continue
                        count += 1
                    max_id = min(tweet_ids)
                    total_count += count
                    print('Total count:', total_count, 'Query num:', queries_count, count)
                if count == 0:
                    break
                queries_count += 1
            except tweepy.error.RateLimitError as e:
                print(e)
                time.sleep(60)
                continue


    for user_id in user_ids:
        user_tweet_count = 0
        try:
            for tweet in api.user_timeline(user_id=user_id, count=100):
                try:
                    tweets_db.save(tweet._json)
                except couchdb.http.ResourceConflict as e:
                    print(e)
                    continue
                user_tweet_count += 1
            total_count += user_tweet_count
            print('Total count:',total_count, 'User id', user_id, user_tweet_count)
        except tweepy.error.TweepError as e:
            print(e)
            continue
    return total_count


def main(argv):
    global server
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
    initial_database(database_name)
    total_count = get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, interested_city)
    print('Get', total_count, 'tweets')


if __name__ == '__main__':
    main(sys.argv[1:])
