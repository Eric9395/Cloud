# Team 20
# Team member: Site Huang, 908282
#              Chenyuan Zhang, 815901
#              Zixuan Zhang, 846305
#              Zhentao Zhang, 864735
#              Kangyun Dou, 740145
from nltk import NaiveBayesClassifier
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
import json
import re
import nltk
import string
from nltk.tokenize import TweetTokenizer
from shapely.geometry import shape, Point


class twitterProcessor():

    def __init__(self):
        nltk.download('twitter_samples')
        nltk.download('stopwords')
        nltk.download('wordnet')
        pos_tweets = twitter_samples.strings('positive_tweets.json')
        neg_tweets = twitter_samples.strings('negative_tweets.json')

        self.stopwords_english = stopwords.words('english')

        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        self.classifier = self.generateModel(pos_tweets, neg_tweets)
        with open('melbourne_suburbs.geojson') as f:
            self.geoJs = json.load(f)

    def locate(self, lon, lat):
        point = Point(lon, lat)
        for feature in self.geoJs['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return feature['properties']['SA2_NAME16']

    def lemmatize(self, word):
        lemma = self.lemmatizer.lemmatize(word, 'v')
        if lemma == word:
            lemma = self.lemmatizer.lemmatize(word, 'n')
        return lemma

    def clean_tweets(self, tweet):
        # Happy Emoticons
        emoticons_happy = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'
        ])

        # Sad Emoticons
        emoticons_sad = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
        ])

        # all emoticons (happy + sad)
        emoticons = emoticons_happy.union(emoticons_sad)
        # remove stock market tickers like $GE
        tweet = re.sub(r'\$\w*', '', tweet)

        # remove old style retweet text "RT"
        tweet = re.sub(r'^RT[\s]+', '', tweet)

        # remove hyperlinks
        tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

        # remove hashtags
        # only removing the hash # sign from the word
        tweet = re.sub(r'#', '', tweet)

        # tokenize tweets
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        tweet_tokens = tokenizer.tokenize(tweet)

        tweets_clean = []
        for word in tweet_tokens:
            if (word not in self.stopwords_english and  # remove stopwords
                # word not in emoticons and  # remove emoticons
                    word not in string.punctuation):  # remove punctuation
                # tweets_clean.append(word)
                lemma_word = self.lemmatize(word)  # stemming word
                tweets_clean.append(lemma_word)

        return tweets_clean

    def bag_of_words(self, tweet):
        words = self.clean_tweets(tweet)
        words_dictionary = dict([word, True] for word in words)
        return words_dictionary

    def generateModel(self, pos_tweets, neg_tweets):
        pos_tweets_set = []
        for tweet in pos_tweets:
            pos_tweets_set.append((self.bag_of_words(tweet), 'pos'))

        neg_tweets_set = []
        for tweet in neg_tweets:
            neg_tweets_set.append((self.bag_of_words(tweet), 'neg'))

        train_set = pos_tweets_set + neg_tweets_set

        return NaiveBayesClassifier.train(train_set)

    def sentimentValue(self, tweetText):
        return self.classifier.prob_classify(self.bag_of_words(tweetText)).prob('pos')
