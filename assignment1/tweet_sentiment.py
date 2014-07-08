import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def sent_dictionary(sent_file):
	scores = {} # initialize an empty dictionary
	for line in sent_file:
		term, score = line.split("\t")
		scores[term] = int(score)

	return scores

def twitterdata_parse(tweet_file):
    #twitters = {}  # store the id and its message
    twitters = []
    for line in tweet_file:
        tweet = json.loads(line)
        if 'id' in tweet.keys() and 'text' in tweet.keys():
            #tweet_id = tweet['id']
            tweet_text = tweet['text'].encode('utf-8')
            twitters.append(tweet_text)
    
    return twitters   


def sentiment(sent_scores, twitter_messages):
    #tweet_scores = {} # store the sentiment score for each tweet
    #for id in twitter_messages.keys():
    for index in range(len(twitter_messages)):
        words = twitter_messages[index].split()
        #tweet_scores[id] = 0
        tweet_score = 0
        for word in words:
            word = word.rstrip('?:!.,;"!@')
            word = word.replace("\n", "")
            if word in sent_scores.keys():
                tweet_score += sent_scores[word]
        print float(tweet_score)
    
        
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
    sentiment(sent_scores, twitter_messages)
    

if __name__ == '__main__':
    main()






