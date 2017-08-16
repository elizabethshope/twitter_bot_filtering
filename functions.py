# Imports
import configparser as ConfigParser


# This is a function that processes a tweet to determine if it has urls and hashtags
# If it has at least one url, has_url = 1; otherwise, has_url = 0
# If it has at least one hashtag, has_ht = 1; otherwise, has_ht = 0
def process_tweet(tweet):
    # Set has_ht to 1 if the tweet has a hashtag, and to 0 otherwise
    if tweet['entities']['urls'] == []:
        has_url = 0
    elif tweet['entities']['urls'][0]['url'] == '':
        has_url = 0
    else:
        has_url = 1

    # Set has_url to 1 if the tweet has a hashtag, and to 0 otherwise
    if tweet['entities']['hashtags'] == []:
        has_ht = 0
    else:
        has_ht = 1
    return has_url, has_ht


# This function iterates through the tweets and creates a dictionary that indicates how many tweets a user has,
# how many of the user's tweets have a hashtag, and how many of the tweets have a url; it returns a dict with this info
def make_user_hashtag_url_portion_dict(tweets):
    user_dict = {}
    for tweet in tweets:
        user = tweet['user']['id']
        if user not in user_dict:
            user_dict[user] = {'count': 0, 'hashtag_count': 0, 'url_count': 0}
        has_url, has_ht = process_tweet(tweet)
        user_dict[user]['count'] += 1
        user_dict[user]['hashtag_count'] += has_ht
        user_dict[user]['url_count'] += has_url
    return user_dict


# This function takes a list of tweets and returns a list of suspected bots
# The default is to find bots based on both the white list and hashtag & url portions,
# but you can set whitelist or hashtag_url to False to avoid using that bot detection method
def find_suspected_bots(tweets, config_file, whitelist=True, hashtag_url=True):
    # Initialize empty sets for the bot ids and screennames
    suspected_bots = set()

    # Get info from the config file
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(config_file)
    source_whitelist = config_parser.get('TwitterParams', 'source_whitelist').split('\n')
    tweet_count_threshold = int(config_parser.get('TwitterParams', 'tweet_count_threshold'))
    min_url_portion = float(config_parser.get('TwitterParams', 'min_url_portion'))
    max_url_portion = float(config_parser.get('TwitterParams', 'max_url_portion'))
    min_hashtag_portion = float(config_parser.get('TwitterParams', 'min_hashtag_portion'))
    max_hashtag_portion = float(config_parser.get('TwitterParams', 'max_hashtag_portion'))

    # Add suspected bots to set -- based on source whitelist
    if whitelist:
        suspected_bots = suspected_bots.union(set([tweet['user']['id'] for tweet in tweets if tweet['source'] not in source_whitelist]))

    # Add suspected bots to set -- based on URL and/or hashtag portions
    if hashtag_url:
        user_dict = make_user_hashtag_url_portion_dict(tweets)
        for user in user_dict:
            if user_dict[user]['count'] < tweet_count_threshold:
                continue
            if user_dict[user]['hashtag_count']/user_dict[user]['count'] <= min_hashtag_portion and \
                    user_dict[user]['url_count']/user_dict[user]['count'] <= min_url_portion:
                suspected_bots.add(user)
            if user_dict[user]['hashtag_count']/user_dict[user]['count'] >= max_hashtag_portion:
                suspected_bots.add(user)
            if user_dict[user]['url_count']/user_dict[user]['count'] >= max_url_portion:
                suspected_bots.add(user)

    # Return sets of suspected bots
    return suspected_bots


# This function takes a list of tweets and returns a list of tweets without tweets from suspected bots
def remove_bot_tweets(tweets, config_file):
    suspected_bots = find_suspected_bots(tweets, config_file, whitelist=True, hashtag_url=True)
    return [tweet for tweet in tweets if tweet['user']['id'] not in suspected_bots]
