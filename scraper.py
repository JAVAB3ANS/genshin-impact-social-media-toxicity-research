import requests, datetime, time
import argparse
import pandas as pd
from langdetect import detect

class TwitterScraper:
    API_HEADERS = {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "x-csrf-token": "0"
    }

    """ 
    
    1. Creates a class called Hashtag
    2. Creates a constructor for the class Hashtag that takes in a parameter called hashtag
    3. Creates a method called __init__ that takes in a parameter called hashtag
    4. Sets the instance variable hashtag to the parameter hashtag 

    """

    def __init__(self, hashtag):
        self.hashtag = hashtag

    """

    1. Sets the parameters for the search query.
    2. The parameters are passed to the search_tweets() function.
    3. The search_tweets() function returns the tweets.
    4. The tweets are stored in the self.tweets variable. 

    """ 

    def set_params(self, scroll_value):
        self.params = (
            ("include_profile_interstitial_type", "1"),
            ("include_blocking", "1"),
            ("include_blocked_by", "1"),
            ("include_followed_by", "1"),
            ("include_want_retweets", "1"),
            ("include_mute_edge", "1"),
            ("include_can_dm", "1"),
            ("include_can_media_tag", "1"),
            ("skip_status", "1"),
            ("cards_platform", "Web-12"),
            ("include_cards", "1"),
            ("include_ext_alt_text", "true"),
            ("include_quote_count", "true"),
            ("include_reply_count", "1"),
            ("tweet_mode", "extended"),
            ("include_entities", "true"),
            ("include_user_entities", "true"),
            ("include_ext_media_color", "true"),
            ("include_ext_media_availability", "true"),
            ("send_error_codes", "true"),
            ("simple_quoted_tweet", "true"),
            ("q", self.hashtag),
            ("tweet_search_mode", "live"),
            ("count", "20"),
            ("query_source", "recent_search_click"),
            ("cursor", scroll_value),
            ("pc", "1"),
            ("spelling_corrections", "1"),
            ("ext", "mediaStats,highlightedLabel"),
        )

    # Thanks Todd Birchard for his awesome json extraction method
    # https://hackersandslackers.com/extract-data-from-complex-json-python/

    """

    1. Recursively searches for values of key in JSON tree.
    2. Returns all values of key in JSON tree.

    """

    def json_extract(self, obj, key):
        """Recursively fetch values from nested JSON."""
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        values = extract(obj, arr, key)
        return values

    """

    1. It sends a POST request to the Twitter API to get a guest token.
    2. It then returns the guest token.

    """

    def get_xguest_token(self):
        guest_token_header = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        }

        r = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers=guest_token_header)
        return r.json()["guest_token"]

    """

    1. Initates the search request with the first scroll value.
    2. Gets the scroll value from the response.
    3. Sets the scroll value in the params for the next request.
    4. Gets the tweets from the response.
    5. Gets the screen name of the user who posted the tweet.
    6. Gets the formatted tweet date.
    7. Prints the tweets.
    8. Saves the tweets to a csv file.
    9. Waits for 10 secs and gets a new guest token.
    10. Repeat steps 1-9 until there are no more tweets. 

    """

    def list_reviews(self):
        print("---------------------------------Tweets Start----------------------------------------------")
        self.set_params("")
        # We need a guest token to search tweets without having a twitter account.
        # Then we'll add that guest token to the header of search request
        self.API_HEADERS["x-guest-token"] = self.get_xguest_token()
        # Initate tweets to an empty list
        tweets = {"globalObjects": {}}
        while (len(tweets) > 0):
            try:
                response = requests.get("https://twitter.com/i/api/2/search/adaptive.json", headers=self.API_HEADERS,
                                        params=self.params)
                #The tweets are located in ["globalObjects"]["tweets"] key
                tweets = response.json()["globalObjects"]["tweets"]
                #I'll also get the screen name of the user who posted that tweet. This is located in ["globalObjects"]["users"] key
                users = response.json()["globalObjects"]["users"]
                #Twitter generates scroll values on the fly and it's located in a key called "value".
                #Therefore we need to search this value until we find it.
                cursor_scroll_value = self.json_extract(response.json(), "value")[1]
                #set this value in the params for request
                self.set_params(cursor_scroll_value)
                names = [] 
                tweet_links = []
                tweet_array = [] 
                tweet_dates = [] 
                retweet_array = []
                favorite_array = []
                replies = []
                quotes = []
                favorited_array = []
                retweeted_array = []
                for tweet in tweets:   
                    if detect(tweets[tweet]["full_text"]) != "en": # if the tweet's full text is not in english
                        continue
                    # Get formatted tweet date
                    tweet_date = datetime.datetime.strftime(
                        datetime.datetime.strptime(tweets[tweet]["created_at"], "%a %b %d %H:%M:%S +0000 %Y"),
                        "%Y-%m-%d") 
                    # Get complete formatted tweet link
                    tweet_link = f"https://twitter.com/{users[str(tweets[tweet]['user_id'])]['screen_name']}/status/{tweets[tweet]['id']}?s=20&t={tweets[tweet]['user_id']}"
                    names.append(users[str(tweets[tweet]["user_id"])]["screen_name"])  
                    tweet_links.append(tweet_link)
                    tweet_array.append(tweets[tweet]["full_text"])
                    tweet_dates.append(tweet_date) 
                    retweet_array.append(tweets[tweet]["retweet_count"])
                    favorite_array.append(tweets[tweet]["favorite_count"])
                    replies.append(tweets[tweet]["reply_count"])
                    quotes.append(tweets[tweet]["quote_count"])
                    favorited_array.append(tweets[tweet]["favorited"])
                    retweeted_array.append(tweets[tweet]["retweeted"])

                df = pd.DataFrame({"ACCOUNT NAME": names, "TWEET LINK": tweet_links, "TWEET": tweet_array, "TWEET DATE": tweet_dates, "RETWEETS": retweet_array, "FAVORITES": favorite_array, "REPLIES": replies, "QUOTES": quotes, "FAVORITED": favorited_array, "RETWEETED": retweeted_array})
                df.to_csv(f"{hashtag}.csv", mode="a", index=False, header=False)
            except:
                # If anything goes wrong, I'll wait for 10 secs and get a new guest token
                time.sleep(10)
                self.API_HEADERS["x-guest-token"] = self.get_xguest_token()

        print("---------------------------------Tweets End-------------------------------------------------")

"""

1. Parses the arguments from the command line.
2. Creates a TwitterScraper object.
3. Calls the list_reviews method on the TwitterScraper object.

"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for a hashtag")
    parser.add_argument("--hashtag", required=True,
                        help="Please enter a hashtag that starts with # symbol")
    args = parser.parse_args()
    hashtag = args.hashtag
    ts = TwitterScraper(hashtag)
    ts.list_reviews()