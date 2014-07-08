import sys
import json

''' 
Get top ten hash tags
  a script that computes the frequency of hash tags in the twitter data
  haoeric, 8 JUL 2014    
'''


# parse the twitter data to extract the id and tweet
def twitterdata_parse(tweet_file):
    hashtag_count = {}  # store the hashtag and its count
    for line in tweet_file:
        tweet = json.loads(line)
        if "entities" in tweet.keys() and "hashtags" in tweet["entities"]:
            if tweet['entities']['hashtags'] != []:
                # append each hashtag (in unicode)
                for hashtag in tweet["entities"]["hashtags"]:
                    unicode_hashtag = hashtag["text"].encode('utf-8')
                    if unicode_hashtag in hashtag_count.keys():
                        hashtag_count[unicode_hashtag] += 1
                    else:
                        hashtag_count[unicode_hashtag] = 1

    return hashtag_count        

def main():
    tweet_file = open(sys.argv[1])

    # read the tweet data and count the frequency of each hashtag
    hashtags = twitterdata_parse(tweet_file)
    tweet_file.close()

    # get the top ten hashtage
    #sorted(d.iteritems(), key=lambda x:-x[1])
    top_ten_tag = sorted(hashtags.iteritems(), key=lambda x:-x[1])[:10]

    # print the top ten hashtags
    for x in top_ten_tag:
        print "{0}: {1}".format(*x)


if __name__ == '__main__':
    main()






