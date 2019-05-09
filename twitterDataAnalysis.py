from nltk import NaiveBayesClassifier
from nltk import classify
from nltk.corpus import twitter_samples
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
import json
import re
import sys
from collections import Counter
import nltk
import string
from nltk.tokenize import TweetTokenizer
from gensim.models import Word2Vec


all_tweets = twitter_samples.strings('tweets.20150430-223406.json')
pos_tweets = twitter_samples.strings('positive_tweets.json')
neg_tweets = twitter_samples.strings('negative_tweets.json')


tweet_tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

stopwords_english = stopwords.words('english')

lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()


def lemmatize(word):
    lemma = lemmatizer.lemmatize(word, 'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word, 'n')
    return lemma


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


def clean_tweets(tweet):
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
        if (word not in stopwords_english and  # remove stopwords
            # word not in emoticons and  # remove emoticons
                word not in string.punctuation):  # remove punctuation
            # tweets_clean.append(word)
            lemma_word = lemmatize(word)  # stemming word
            tweets_clean.append(lemma_word)

    return tweets_clean


def bag_of_words(tweet):
    words = clean_tweets(tweet)
    words_dictionary = dict([word, True] for word in words)
    return words_dictionary


pos_tweets_set = []
for tweet in pos_tweets:
    pos_tweets_set.append((bag_of_words(tweet), 'pos'))

neg_tweets_set = []
for tweet in neg_tweets:
    neg_tweets_set.append((bag_of_words(tweet), 'neg'))

train_set = pos_tweets_set + neg_tweets_set

classifier = NaiveBayesClassifier.train(train_set)


def sentimentValue(tweetText):
    return classifier.prob_classify(bag_of_words(tweetText)).prob('pos')


twitter_file = 'tinyTwitter.json'

with open(twitter_file, 'r') as f:
    for index, line in enumerate(f):

            # simple way to get json-style string in a line
            # twitter = json.loads(re.search(r'.*\}', line).group())
        try:

            # need to remove comma and end of line if needed
            twitter = json.loads(line.rstrip('\n').rstrip(','))
            print(classifier.prob_classify(bag_of_words(twitter['doc']['text'])).prob('pos'))
        except:
            continue
