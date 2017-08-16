# Twitter Bot Filtering

## Intro & Motivation
This repository contains code to help filter out Twitter bots.

Tweets from Twitter bots can make it extremely challenging to find meaningful signals in Twitter data. There are a wide range of purposes of Twitter bots. Some are benevolent bots that share information about topics such as weather and job postings. Others are more nefarious and deceptive, with purposes such as influencing elections or directing people to porn sites.

A number of researchers have used labeled data sets to create classifiers to try to identify certain types of bots. This work is important, especially for identifying more complex bots. There are projects like Indiana University's Botometer (https://botometer.iuni.iu.edu/#!/) -- previously known as "Bot or Not." 

Acquiring labeled training data can be expensive and time consuming. And there are some bots that can be filtered out with simpler methods. 

The code in this repository is a work in progress and will ultimately contain several reasonably fast methods for filtering out tweets from bots. 

## Source Whitelisting
One method of finding and removing tweets from bots is by looking at the "source" of the tweet. Bots publish tweets via the Twitter API, and often their source is revealing. Humans typically post tweets via Tweet via Twitter for Web, Twitter for iPhone, Twitter for Android, or several other platforms that can cross-post to Twitter like Instagram and Foursquare. Benevolent bots, on the other hand, often have sources such as "TweetMyJobs." Thus, one (albeit imperfect) method of filtering out tweets from bots is to create a source whitelist, and remove tweets that are from sources not on the source whitelist. 

## Abnormal Portions of Tweets with Hashtags or URLs
Humans who tweet typically have some tweets that contain hashtags and/or URLs. Some bots have abnormal portions of tweets with hashtags and/or URLs. For example, some job posting bots have hashtags and URLs in 100% of their tweets -- in an effort to have more people find the tweets and direct them to the job posts. Other bots post snippets of poetry or weather information, and 0% of their tweets contain URLs or hashtags. Such a high level of consistency would be unexpected from a human. Thus, we can filter out users with abnormally high or low portions of tweets with URLs and/or hashtags; it is best to couple this with a threshold quantity of tweets from the user as it would be easy for a user with only one or two tweets to have all or none of them contain hashtags and/or URLs. 
