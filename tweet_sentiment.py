"""
Assignment 1 Coursera 2013 - Introduction to Data Science
Compute the sentiment of each tweet based on the sentiment scores of the terms in the
tweet. Each word or phrase found in a tweet, but not in AFINN-111.txt should be given
a sentiment score of 0.
Example:
$ python tweet_sentiment.py AFINN-111.txt output_first_20.txt
0.0
0.0
0.0
0.0
0.0
0.0
-1.0
...
"""
import sys
import json


def get_sentiment_dictionary(sentiment_file):
    """Parse sentiment file, returns a {word: sentiment} dict"""
    sentiment_dictionary = {}
    file = open(sentiment_file)
    for line in file:
        word, sentiment_score = line.split('\t')
        sentiment_dictionary[word] = int(sentiment_score)

    return sentiment_dictionary


def get_tweet_list(tweet_file):
    """Creates a dictionary that stores the tweets"""
    tweet_list = []

    file = open(tweet_file)
    for line in file:
        tweet_list.append(json.loads(line))

    return tweet_list


def get_tweet_sentiment_score(tweet_text, sentiment_dictionary):
    """Returns the score for a tweet or 0 if it's not in AFINN-111.txt"""
    score = 0
    for word in tweet_text.split():
        word = word.rstrip('?:!.,;"!@')
        word = word.replace("\n", "")
        score += sentiment_dictionary.get(word, 0)

    return score


def get_all_tweet_sentiment_scores(tweet_list, sentiment_dictionary):
    """Calculate scores for all tweets in tweet_file"""
    score_array = []
    for i in range(len(tweet_list)):
        if "text" in tweet_list[i]:
            tweet_text = tweet_list[i]["text"]
            score_array.append(get_tweet_sentiment_score(tweet_text, sentiment_dictionary))

    return score_array


if __name__ == '__main__':
    afinn_file = sys.argv[1]
    tweet_file = sys.argv[2]
    sentiment_dictionary = get_sentiment_dictionary(sentiment_file=afinn_file)
    tweet_list = get_tweet_list(tweet_file)
    for tweet_score in get_all_tweet_sentiment_scores(tweet_list=tweet_list, sentiment_dictionary=sentiment_dictionary):
        sys.stdout.writelines('{0}.0\n'.format(tweet_score))
