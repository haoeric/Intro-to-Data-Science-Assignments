import sys
import json

''' 
Derive the sentiment of new terms from the twitter data
  a script that computes the sentiment for the terms that do not appear in the file AFINN-111.txt.
  haoeric, 8 JUL 2014    
'''

# build the dicionary of sentiment of each word form the AFINN-111 file
def sent_dictionary(sent_file):
    scores = {}  # initialize an empty dictionary
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = float(score)

    return scores


# parse the twitter data to extract the id and tweet
def twitterdata_parse(tweet_file):
    twitters = {}  # store the id and its message
    for line in tweet_file:
        tweet = json.loads(line)
        if 'id' in tweet.keys() and 'text' in tweet.keys():
            tweet_id = tweet['id']
            tweet_text = tweet['text'].encode('utf-8')
            twitters[tweet_id] = tweet_text

    return twitters


# evaluate the sentiment score of each tweet
def sentiment_score(sent_scores, twitter_messages):
    tweet_scores = {}  # store the sentiment score for each tweet
    for id in twitter_messages.keys():
        words = twitter_messages[id].split()
        tweet_scores[id] = 0
        for word in words:
            word = word.rstrip('?:!.,;"!@')
            word = word.replace("\n", "")
            if word in sent_scores.keys():
                tweet_scores[id] += sent_scores[word]

    return tweet_scores


# Derive the sentiment of new terms
def term_sentiment(sent_scores, twitter_messages, tweet_scores):
    new_term_sent = {}

    for id in twitter_messages.keys():
        score = tweet_scores[id]
        words = twitter_messages[id].split()
        for word in words:
            word = word.strip('?:!.,;"!@')
            word = word.replace("\n", "")
            if word not in sent_scores.keys():
                if word in new_term_sent.keys():
                    new_term_sent[word] += score
                else:
                    new_term_sent[word] = score
    return new_term_sent


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # read the AFINN-111 data into a dictionary
    sent_scores = sent_dictionary(sent_file)
    sent_file.close()
    # read the tweet data into a dictionary
    twitter_messages = twitterdata_parse(tweet_file)
    tweet_file.close()

    # get the sentiment scores of each tweet message
    tweet_scores = sentiment_score(sent_scores, twitter_messages)

    # Derive the sentiment of new terms
    new_term_sent = term_sentiment(sent_scores, twitter_messages, tweet_scores)

    # print the sentiment score of new terms
    for term in new_term_sent.keys():
        print term, new_term_sent[term]


if __name__ == '__main__':
    main()






