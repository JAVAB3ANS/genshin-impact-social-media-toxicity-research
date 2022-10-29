import pandas as pd 
import re
from textblob import TextBlob
import matplotlib.pyplot as plt 

def cleanTweet(tweet): # function to clean tweet
    # Remove Links, Special Characters etc from tweet
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet.encode("utf-8")).split())

# function to calculate percentage
def percentage(part, whole):  
    return (part / whole) * 100

def plotPieChart(positive, negative, neutral, searchTerm, noOfSearchTerms): # function to plot pie chart
    labels = [f"Positive [{str(positive)}%]", f"Neutral [{str(neutral)}%]",
                f"Negative [{str(negative)}%]"] # labels for the pie chart
    sizes = [positive, neutral, negative] # sizes of the slices
    colors = ["lightgreen", "lightblue", "salmon"] # green, blue, red
    patches, texts = plt.pie(sizes, colors=colors, startangle=90) # startangle = 90 means that the pie chart will be divided into three parts
    plt.legend(patches, labels, loc="best") # add legend to the plot
    plt.title(f"Overall user sentiments of {str(noOfSearchTerms)} {searchTerm} tweets.") # title of the pie chart
    plt.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout() # to make the pie chart look perfect
    plt.show() # show the pie chart

if __name__ == "__main__":
    # creating some variables to store info
    polarity = 1 # polarity of the tweet
    positive = 0 # positive tweets
    negative = 0 # negative tweets
    neutral = 0 # neutral tweets

    df = pd.read_csv("./#boycottgenshin.csv") # read the csv file

    # iterate through the tweets in the csv file
    # add a column to the csv file to store the polarity of each tweet
    df["POLARITY"] = [TextBlob(cleaned_tweet).sentiment.polarity for cleaned_tweet in df["TWEET"]] 

    for index, row in df.iterrows(): # iterating over the data frame
        polarity = row["POLARITY"] # getting the polarity of each tweet
        if (polarity > 0): # adding reaction of how people are reacting to find average later
            positive += 1.0 # adding to positive
        elif (polarity == 0): # adding reaction of how people are reacting to find average later
            neutral += 1.0 # adding to neutral
        else: # adding reaction of how people are reacting to find average later
            negative += 1.0 # adding to negative

    positive = percentage(positive, len(df["TWEET"])) # finding the percentage of positive tweets
    negative = percentage(negative, len(df["TWEET"])) # finding the percentage of negative tweets
    neutral = percentage(neutral, len(df["TWEET"])) # finding the percentage of neutral tweets

    # finding average reaction
    polarity = polarity / (df.shape[0] - 1) # polarity of the tweet

    # printing out data
    print("\n\nOutput:     ")
    print(f"Overall user sentiments of {str(df.shape[0] - 1)} #boycottgenshin tweets.")
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

    plotPieChart(positive, negative, neutral, "#boycottgenshin", df.shape[0] - 1) # calling the function to plot pie chart