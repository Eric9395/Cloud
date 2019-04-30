import couchdb
import tweepy
import time
import sys


def initial_database(couchdb_username, couchdb_password, database_name):
    global server, tweets_db
    server = couchdb.Server('http://'+couchdb_username+':'+couchdb_password+'@127.0.0.1:5984/')
    try:
        tweets_db = server[database_name]
    except couchdb.http.ResourceNotFound as e:
        server.create(database_name)
        tweets_db = server[database_name]


def get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, interested_city):
    total_count = 0
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    user_ids = []
    api = tweepy.API(auth)

    places = api.geo_search(query=interested_city)
    places_info = []
    places_name = []
    for place in places:
        if place.country_code == 'AU' and place.full_name not in places_name:
            #[x_min, x_max, y_min, y_max]
            # bounding_box = []
            # bounding_box.append(place.bounding_box.coordinates[0][0][0])
            # bounding_box.append(place.bounding_box.coordinates[0][2][0])
            # bounding_box.append(place.bounding_box.coordinates[0][0][1])
            # bounding_box.append(place.bounding_box.coordinates[0][2][1])
            places_info.append((place.full_name, place.id))
            places_name.append(place.full_name)
            break

    userids = open('userids.txt', 'r', encoding='UTF-8')
    tweets = open('tweet.txt', 'a', encoding='UTF-8')
    for line in userids.readlines():
        user_ids.append(line.strip())
    print('Total users num:', len(user_ids))
    for user_id in user_ids:
        user_tweet_count = 0
        try:
            for tweet in api.user_timeline(user_id=user_id, count=100):
                try:
                    if tweet._json['place']:
                        if tweet._json['place']['full_name'] == places_info[0][0]:

                            user_tweet_count += 1
                except couchdb.http.ResourceConflict as e:
                    print(e)
                    continue

            total_count += user_tweet_count
            print('Total count:',total_count, 'User id', user_id, user_tweet_count)
        except tweepy.error.TweepError as e:
            print(e)
            continue
    return total_count


def main(argv):
    if len(argv) < 8:
        print('command: <consumer_key> <consumer_secret> <access_token> <access_token_secret> '
              '<interested_city> <couchdb_username> <couchdb_password> <database_name>')
        sys.exit(2)
    consumer_key = argv[0]
    consumer_secret = argv[1]
    access_token = argv[2]
    access_token_secret = argv[3]
    interested_city = argv[4]
    couchdb_username = argv[5]
    couchdb_password = argv[6]
    database_name = argv[7]
    initial_database(couchdb_username, couchdb_password, database_name)

    total_count = get_tweet(consumer_key, consumer_secret, access_token, access_token_secret, interested_city)
    print('Get', total_count, 'tweets')


if __name__ == '__main__':
    main(sys.argv[1:])
