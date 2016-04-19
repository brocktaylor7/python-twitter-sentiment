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


def get_tweet_sentiment_score(word_list, sentiment_dictionary):
    """Returns the score for a tweet or 0 if it's not in AFINN-111.txt"""
    score = 0
    for word in word_list:
        score += sentiment_dictionary.get(word, 0)

    return score


def get_clean_word_list(tweet_text):
    word_list = []
    for word in tweet_text.split():
        word = word.rstrip('?:!.,;"!@')
        word = word.replace("\n", "")
        word = word.lower()
        word_list.append(word)

    return word_list


def assign_score_to_unknown_terms(word_list, tweet_score, sentiment_dictionary, new_term_sentiment_dictionary):
    for word in word_list:
        if word not in sentiment_dictionary:
            if word in new_term_sentiment_dictionary:
                new_term_sentiment_dictionary[word]["total_score"] += float(tweet_score)
                new_term_sentiment_dictionary[word]["frequency"] += 1
                new_term_sentiment_dictionary[word]["score"] = float(
                    new_term_sentiment_dictionary[word]["total_score"] / new_term_sentiment_dictionary[word]["frequency"]
                )
            else:
                new_term_sentiment_dictionary[word] = {
                    "total_score": float(tweet_score),
                    "frequency": 1,
                    "score": float(tweet_score)
                }
                # new_term_sentiment_dictionary[word]["total_score"] = tweet_score
                # new_term_sentiment_dictionary[word]["frequency"] = 1
                # new_term_sentiment_dictionary[word]["score"] = tweet_score

    return new_term_sentiment_dictionary


def calculate_unknown_term_sentiment(tweet_list, sentiment_dictionary):
    new_term_sentiment_dictionary = {}
    for i in range(len(tweet_list)):
        if "text" in tweet_list[i]:
            word_list = get_clean_word_list(tweet_list[i]["text"])
            tweet_score = get_tweet_sentiment_score(word_list, sentiment_dictionary)

            if tweet_score != 0:
                new_term_sentiment_dictionary = assign_score_to_unknown_terms(word_list, tweet_score,
                                                                              sentiment_dictionary,
                                                                              new_term_sentiment_dictionary)

    return new_term_sentiment_dictionary


def main():
    afinn_file = sys.argv[1]
    tweet_file = sys.argv[2]

    sentiment_dictionary = get_sentiment_dictionary(sentiment_file=afinn_file)
    tweet_list = get_tweet_list(tweet_file=tweet_file)

    new_term_sentiment_dictionary = calculate_unknown_term_sentiment(tweet_list=tweet_list,
                                                                     sentiment_dictionary=sentiment_dictionary)

    for term in sorted(new_term_sentiment_dictionary):
        sys.stdout.writelines('{0} {1}\n'.format(term.encode('utf-8'), new_term_sentiment_dictionary[term]["score"]))


if __name__ == '__main__':
    main()
