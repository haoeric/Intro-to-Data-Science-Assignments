import sys
import json

''' 
Compute Term Frequency
  a script that computes the frequency of each unique term in the twitter data
  haoeric, 8 JUL 2014    
'''


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




# Derive the sentiment of new terms
def frequency_calculate(twitter_messages):
    term_count = {}
    term_freq = {}

    for id in twitter_messages.keys():
        words = twitter_messages[id].split()
        for word in words:
            word = word.strip('?:!.,;"!@')
            word = word.replace("\n", "")
            if word in term_count.keys():
                term_count[word] += 1
            else:
                term_count[word] = 1
                
    total_count = sum(term_count.values())
    
    for term in term_count.keys():
        term_freq[term] = "%.3f" %(float(term_count[term]) / total_count)
     
    return term_freq           

def main():
    tweet_file = open(sys.argv[1])

    # read the tweet data into a dictionary
    twitter_messages = twitterdata_parse(tweet_file)
    tweet_file.close()

    # get the frequency of each unique term
    term_frequency = frequency_calculate(twitter_messages)

    # print the frequency of unique items
    for term in term_frequency.keys():
        print term, term_frequency[term]


if __name__ == '__main__':
    main()






