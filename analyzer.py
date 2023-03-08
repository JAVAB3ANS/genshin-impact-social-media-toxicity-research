import pandas as pd 
import re
from textblob import TextBlob
import matplotlib.pyplot as plt 
import nltk
 
nltk.download("words")
words = set(nltk.corpus.words.words())

class SentimentAnalysis:
    # function to analyze sentiments of passed tweet using textblob's sentiment method
    def analyzeSentiments(self):
        polarity = 1
        positive = 0
        negative = 0
        neutral = 0
        
        df = pd.read_csv("./#boycottgenshin.csv", dtype={"third_column": "str"}, low_memory=False)

        df["POLARITY"] = [TextBlob(self.cleanTweet(cleaned_tweet)).sentiment.polarity for cleaned_tweet in df["TWEET"]]

        for index, row in df.iterrows():
            polarity = row["POLARITY"]
            if (polarity > 0):
                positive += 1.0
            elif (polarity == 0):
                neutral += 1.0
            else:
                negative += 1.0

        positive = self.percentage(positive, len(df["TWEET"]))
        negative = self.percentage(negative, len(df["TWEET"]))
        neutral = self.percentage(neutral, len(df["TWEET"]))

        polarity = polarity / (df.shape[0] - 1)

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

        self.plotPieChart(positive, negative, neutral, "#boycottgenshin", df.shape[0] - 1)

    # function to clean tweets 
    def cleanTweet(self, tweet):
        if type(tweet) == float:
            return ""
        temp = self.deEmojify(tweet).lower()
        temp = re.sub("'", "", temp)
        temp = re.sub("@[A-Za-z0-9_]+","", temp)
        temp = re.sub("#[A-Za-z0-9_]+","", temp)
        temp = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", temp)
        temp = re.sub('[()!?]', " ", temp)
        temp = re.sub('\[.*?\]'," ", temp)
        temp = re.sub("[^a-z0-9]"," ", temp)
        temp = " ".join(w for w in nltk.wordpunct_tokenize(temp) \
         if w.lower() in words or not w.isalpha())
        temp = temp.split()
        temp = " ".join(word for word in temp)
        return temp 

    # function to remove emojis
    def deEmojify(self, text):
        regex_pattern = re.compile(pattern = "[" 
            u"\U0001F600-\U0001F64F"  
            u"\U0001F300-\U0001F5FF"  
            u"\U0001F680-\U0001F6FF"  
            u"\U0001F1E0-\U0001F1FF"  
                            "]+", flags = re.UNICODE)
        return regex_pattern.sub(r'',text)

    # function to calculate percentage
    def percentage(self, part, whole):  
        return (part / whole) * 100
    
    # function to plot pie chart
    def plotPieChart(self, positive, negative, neutral, searchQuery, noOfSearchTerms): 
        labels = ['Positive ['+str(positive)+'%]', 'Neutral ['+str(neutral)+'%]', 'Negative ['+str(negative)+'%]']
        sizes = [positive, neutral, negative]
        colors = ['yellowgreen','gold','red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchQuery + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.analyzeSentiments()