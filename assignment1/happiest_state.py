import sys
import json

''' 
Which State is happiest in USA
  a script that computes the average sentiment scores in each state of USA and find the happiest city
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
def twitterdata_parse(states, tweet_file):
    twitters = {}  # store the id and its message
    twitter_states = {} # store the state of the message
    for line in tweet_file:
        tweet = json.loads(line)
        if all(k in tweet.keys() for k in ("text","id","place")):
            if tweet['place'] is not None and "country_code" in tweet['place'].keys():
                if tweet['place']['country_code'] in states.keys():
                    tweet_id = tweet['id']
                    tweet_text = tweet['text'].encode('utf-8')
                    tweet_state = tweet['place']['country_code']
                    twitters[tweet_id] = tweet_text
                    twitter_states[tweet_id] = tweet_state 
                    

    return (twitters, twitter_states)

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
    
# calculate the average sentiment score of each state in USA
def avg_state_sent(tweet_scores, twitter_states, states):
    state_tweet_count = {}  # count the tweets of each state
    state_sent = {}         # the average sentiment score of each state
    for id in twitter_states.keys():
        state = twitter_states[id]
        score = tweet_scores[id]
        if state in state_sent.keys():
            state_sent[state] += score
            state_tweet_count[state] += 1
        else:
            state_sent[state] = score
            state_tweet_count[state] = 1
    
    for s in state_sent.keys():
        state_sent[s] = state_sent[s] / state_tweet_count[s]
        
    return state_sent
    

def main():
    
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # read the AFINN-111 data into a dictionary
    sent_scores = sent_dictionary(sent_file)
    sent_file.close()
    # read the tweet data into a dictionary
    (twitter_messages, twitter_states) = twitterdata_parse(states, tweet_file)
    tweet_file.close()

    # get the sentiment scores of each tweet message
    tweet_scores = sentiment_score(sent_scores, twitter_messages)
    
    # get the average sentiment score of each state
    avg_scores = avg_state_sent(tweet_scores, twitter_states,states)
   

    # print the happiest state
    max_sent = max(avg_scores.values())
    for k,v in avg_scores.items():
        if v==max_sent:
            happiest_state = k 
    
    print happiest_state


if __name__ == '__main__':
    main()







