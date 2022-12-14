import pandas as pd 
import re
from textblob import TextBlob
import matplotlib.pyplot as plt 
import nltk
nltk.download("words")
words = set(nltk.corpus.words.words())

class SentimentAnalysis: # Class to perform sentiment analysis on the tweets
    def analyzeSentiments(self): # function to analyze sentiments
        # creating some variables to store info
        polarity = 1 # polarity of the tweet
        positive = 0 # positive tweets
        negative = 0 # negative tweets
        neutral = 0 # neutral tweets

        df = pd.read_csv("./#boycottgenshin.csv", dtype={"third_column": "str"}, low_memory=False) # read the csv file

        # iterate through the tweets in the csv file
        # add a column to the csv file to store the polarity of each tweet
        df["POLARITY"] = [TextBlob(self.cleanTweet(cleaned_tweet)).sentiment.polarity for cleaned_tweet in df["TWEET"]]  

        for index, row in df.iterrows(): # iterating over the data frame
            polarity = row["POLARITY"] # getting the polarity of each tweet
            if (polarity > 0): # adding reaction of how people are reacting to find average later
                positive += 1.0 # adding to positive
            elif (polarity == 0): # adding reaction of how people are reacting to find average later
                neutral += 1.0 # adding to neutral
            else: # adding reaction of how people are reacting to find average later
                negative += 1.0 # adding to negative

        positive = self.percentage(positive, len(df["TWEET"])) # finding the percentage of positive tweets
        negative = self.percentage(negative, len(df["TWEET"])) # finding the percentage of negative tweets
        neutral = self.percentage(neutral, len(df["TWEET"])) # finding the percentage of neutral tweets

        # finding average reaction
        polarity = polarity / (df.shape[0] - 1) # polarity of the tweet

        # printing out data
        print("\n\nOutput:     ")
        print(f"Overall user sentiments of {str(df.shape[0] - 1)} #boycottgenshin tweets")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0):
            print("Positive")
        elif (polarity < 0):
            print("Negative")

        print()
        print("Detailed Report: ")
        print(f"{str(positive)}% people thought it was positive")
        print(f"{str(negative)}% people thought it was negative")
        print(f"{str(neutral)}% people thought it was neutral")

        self.plotPieChart(positive, negative, neutral, "#boycottgenshin", df.shape[0] - 1) # calling the function to plot pie chart

    def cleanTweet(self, tweet): # function to clean the tweet
        # Remove Links, Special Characters etc from tweet
        if type(tweet) == float:
            return ""
        temp = self.deEmojify(tweet).lower()
        temp = re.sub("'", "", temp) # to avoid removing contractions in english
        temp = re.sub("@[A-Za-z0-9_]+","", temp) # remove @mentions
        temp = re.sub("#[A-Za-z0-9_]+","", temp) # remove #hashtags
        temp = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", temp) # remove hyperlinks
        temp = re.sub('[()!?]', " ", temp) # remove special characters
        temp = re.sub('\[.*?\]'," ", temp) # remove special characters
        temp = re.sub("[^a-z0-9]"," ", temp) # remove special characters
        temp = " ".join(w for w in nltk.wordpunct_tokenize(temp) \
         if w.lower() in words or not w.isalpha()) #Remove non-english tweets (not 100% success)
        temp = temp.split() # split the tweet into words
        temp = " ".join(word for word in temp) # join the words to make a sentence
        return temp 

    def deEmojify(self, text): # function to remove emojis from the tweet
        regex_pattern = re.compile(pattern = "[" 
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags = re.UNICODE)
        return regex_pattern.sub(r'',text)

    # function to calculate percentage
    def percentage(self, part, whole):  
        return (part / whole) * 100

    def plotPieChart(self, positive, negative, neutral, searchTerm, noOfSearchTerms): # function to plot pie chart
        labels = [f"Positive [{str(positive)}%]", f"Neutral [{str(neutral)}%]",
                    f"Negative [{str(negative)}%]"] # labels for the pie chart
        sizes = [positive, neutral, negative] # sizes of the slices
        colors = ["lightgreen", "lightblue", "salmon"] # green, blue, red
        patches, texts = plt.pie(sizes, colors=colors, startangle=90) # startangle = 90 means that the pie chart will be divided into three parts
        plt.legend(patches, labels, loc="best") # add legend to the plot
        plt.title(f"Overall user sentiments of {str(noOfSearchTerms)} {searchTerm} tweets") # title of the pie chart
        plt.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout() # to make the pie chart look perfect
        plt.show() # show the pie chart 

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.analyzeSentiments()