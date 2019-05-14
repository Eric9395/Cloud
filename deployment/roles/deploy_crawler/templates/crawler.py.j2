# Team 20
# Team member: Site Huang, 908282
#              Chenyuan Zhang, 815901
#              Zixuan Zhang, 846305
#              Zhentao Zhang, 864735
#              Kangyun Dou, 740145

import couchdb
import tweepy
import time
import sys
import twitterProcessor
import viewGenerator


def initial_database(couchdb_ip, couchdb_username, couchdb_password, database_name):
    global server, tweets_db, tp, positive_db, negative_db, vg, vgp, vgn
    server = couchdb.Server('http://'+couchdb_username+':'+couchdb_password+'@'+couchdb_ip+':5984/')
    try:
        positive_db = server['positive_database']
    except couchdb.http.ResourceNotFound as e:
        server.create('positive_database')
        positive_db = server['positive_database']

    try:
        negative_db = server['negative_database']
    except couchdb.http.ResourceNotFound as e:
        server.create('negative_database')
        negative_db = server['negative_database']

    try:
        tweets_db = server[database_name]
    except couchdb.http.ResourceNotFound as e:
        server.create(database_name)
        tweets_db = server[database_name]

    tp = twitterProcessor.twitterProcessor()
    vg = viewGenerator.viewGenerator(couchdb_ip, couchdb_username, couchdb_password, database_name)
    vgp = viewGenerator.viewGenerator(couchdb_ip, couchdb_username,
                                      couchdb_password, 'positive_database')
    vgn = viewGenerator.viewGenerator(couchdb_ip, couchdb_username,
                                      couchdb_password, 'negative_database')


def get_tweet(consumer_key, consumer_secret, access_token, access_token_secret,
              interested_city, MAX_THRESHOLD, MIN_THRESHOLD):
    total_count = 0
    conflict_num = 0
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    places = api.geo_search(query=interested_city)
    places_ids = []
    places_name = []
    for place in places:
        if place.country_code == 'AU' and place.place_type == 'city':
            places_ids.append((place.full_name, place.id))
            places_name.append(place.full_name)
    user_ids = set()
    for place_id in places_ids:
        print(place_id[0], place_id[1])
        max_id = float('inf')
        tweet_ids = []
        queries_count = 0
        i = 0
        while True:
            try:
                count = 0
                for tweet in api.search(q="place:%s" % place_id[1], count=100, max_id=max_id-1):
                    count += 1
                    tweet_ids.append(tweet.id)
                    user_ids.add(str(tweet._json['user']['id']))

                    tweet._json['_id'] = str(tweet.id)
                    text = tweet._json['text']
                    score = tp.sentimentValue(text)
                    tweet._json['wrath_score'] = score
                    if tweet._json['coordinates']:
                        surburb_name = tp.locate(tweet._json['coordinates']['coordinates'][0],
                                                 tweet._json['coordinates']['coordinates'][1])
                    else:
                        x_min = tweet.place.bounding_box.coordinates[0][0][0]
                        x_max = tweet.place.bounding_box.coordinates[0][1][0]
                        y_min = tweet.place.bounding_box.coordinates[0][0][1]
                        y_max = tweet.place.bounding_box.coordinates[0][2][1]
                        x = (x_min+x_max)/2.0
                        y = (y_min+y_max)/2.0
                        surburb_name = tp.locate(x,y)

                    if surburb_name:
                        tweet._json['place']['full_name'] = surburb_name

                    try:
                        if score > MAX_THRESHOLD:
                            positive_db.save(tweet._json)
                        elif score < MIN_THRESHOLD:
                            negative_db.save(tweet._json)
                        tweets_db.save(tweet._json)
                    except couchdb.http.ResourceConflict as e:
                        print(e)
                        conflict_num += 1
                        continue
                    except ConnectionRefusedError as e:
                        print(e)
                        time.sleep(10)
                        continue
                max_id = min(tweet_ids)
                total_count += count
                print('Total count:', total_count, 'Query num:', queries_count, count)
                if count == 0:
                    break
                queries_count += 1
            except tweepy.error.RateLimitError as e:
                print(e)
                print('Update view')
                vg.updateView()
                vgp.updateView()
                vgn.updateView()
                time.sleep(900)
                continue
    print('Total users num:', len(user_ids))
    for user_id in user_ids:
        user_tweet_count = 0
        try:
            for tweet in api.user_timeline(user_id=user_id, count=100):
                try:
                    if tweet._json['place']:
                        if tweet._json['place']['full_name'] == places_ids[0][0]:
                            tweet._json['_id'] = str(tweet.id)
                            text = tweet._json['text']
                            score = tp.sentimentValue(text)
                            tweet._json['wrath_score'] = score

                            if tweet._json['coordinates']:
                                surburb_name = tp.locate(tweet._json['coordinates']['coordinates'][0],
                                                         tweet._json['coordinates']['coordinates'][1])
                            else:
                                x_min = tweet.place.bounding_box.coordinates[0][0][0]
                                x_max = tweet.place.bounding_box.coordinates[0][1][0]
                                y_min = tweet.place.bounding_box.coordinates[0][0][1]
                                y_max = tweet.place.bounding_box.coordinates[0][2][1]
                                x = (x_min + x_max) / 2.0
                                y = (y_min + y_max) / 2.0
                                surburb_name = tp.locate(x, y)
                            if surburb_name:
                                tweet._json['place']['full_name'] = surburb_name

                            if score > MAX_THRESHOLD:
                                positive_db.save(tweet._json)
                            elif score < MIN_THRESHOLD:
                                negative_db.save(tweet._json)
                            tweets_db.save(tweet._json)
                            user_tweet_count += 1
                except couchdb.http.ResourceConflict as e:
                    print(e)
                    continue
                except ConnectionRefusedError as e:
                    print(e)
                    time.sleep(10)
                    continue
            total_count += user_tweet_count
            print('Total count:', total_count, 'User id', user_id, user_tweet_count)
        except tweepy.error.RateLimitError as e:
            print(e)
            print('Update view')
            vg.updateView()
            vgp.updateView()
            vgn.updateView()
            time.sleep(900)
            continue
        except tweepy.error.TweepError as e:
            print(e)
            continue
    return total_count


def main(argv):
    if len(argv) < 9:
        print('command: <consumer_key> <consumer_secret> <access_token> <access_token_secret> <interested_city> '
              '<couchdb_ip> <couchdb_username> <couchdb_password> <database_name>')
        sys.exit(2)
    MAX_THRESHOLD = 0.8
    MIN_THRESHOLD = 0.2
    consumer_key = argv[0]
    consumer_secret = argv[1]
    access_token = argv[2]
    access_token_secret = argv[3]
    interested_city = argv[4]
    couchdb_ip = argv[5]
    couchdb_username = argv[6]
    couchdb_password = argv[7]
    database_name = argv[8]
    initial_database(couchdb_ip, couchdb_username, couchdb_password, database_name)
    total_count = get_tweet(consumer_key, consumer_secret, access_token, access_token_secret,
                            interested_city, MAX_THRESHOLD, MIN_THRESHOLD)
    print('Get', total_count, 'tweets')


if __name__ == '__main__':
    main(sys.argv[1:])
