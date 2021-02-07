import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import tweepy as tw
from config import consumer_key, consumer_secret, access_token, access_token_secret, twitter_lang
from textblob import TextBlob
import re

# Establish a connection and authorize with the Firestore database.
def initialize_firestore():
    cred = credentials.Certificate('/Users/cadenfranc/Documents/Git/firestore-application/service-account-file.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()


# Gather a defined number of recent tweets containing 
# specified key words and upload them to the database.
def update_db(db, key_words, start_date, items):
    print("Gathering tweets from twitter...")
    tweets = tw.Cursor(api.search, q=key_words, lang=twitter_lang, since=start_date).items(items)
    for tweet in tweets:
        db.collection("twitter_data").document().set({"user" : tweet.user.screen_name, "tweet" : tweet.text})
    print("Database has been updated.")


# Display all tweets stored in the database.
def display_db(db):
    print("Gathering tweets from database...")
    tweets = db.collection("twitter_data").where(u'user', u'!=', u'NULL').get()
    for tweet in tweets:
        print(tweet.to_dict())


# Formats twitter text for processing.
def data_cleanup(tweet):
    # Remove all links, hashtags, mentions, and punctuation from the tweet.
    # Courtesy of https://medium.com/analytics-vidhya/working-with-twitter-data-b0aa5419532
    # Author: Svitlana Galeshchuk
    tweet = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '', tweet, flags=re.MULTILINE)
    tweet = ' '.join(re.sub("([^-9A-Za-z \t])|(\w+:\/\/\S+)","",tweet).split())
    return tweet


# Determines a mean sentiment value for stored tweets.
def calculate_sentiment(db):
    # Get all tweets from database.
    tweets = db.collection("twitter_data").where(u'user', u'!=', u'NULL').get()

    # Create a list of the sentiment values of each tweet in the database.
    sentiment_values = []
    for tweet in tweets:
        sentiment_values.append(TextBlob(data_cleanup(tweet.to_dict().get('tweet'))).polarity)
    
    # Calculate the average sentiment and display it.
    average_sentiment = float(format((sum(sentiment_values) / len(sentiment_values)), '.2f'))
    print(average_sentiment)

    # Display the meaning of the value returned.
    if average_sentiment >= 0.25:
        print("Generally positive.")
    elif average_sentiment <= -0.25:
        print("Generally negative.")
    else:
        print("Generally neutral.")

# Manual override to edit the tweet of a given user.
def modify_db(db, screen_name, tweet):
    db.collection("twitter_data").document().set({"user" : screen_name, "tweet" : tweet})
    print("Tweet for user " + user + " has been manually modified.")
    

# Delete the contents of the database.
def delete_db(db):
    print("Deleting tweets...")
    tweets = db.collection("twitter_data").where(u'user', u'!=', u'NULL').get()
    for tweet in tweets:
        db.collection("twitter_data").document(tweet.id).delete()
    print("Database has been deleted.")


def display_table():
    print("""
    1. Update database.
    2. Display information from database.
    3. Calculate sentiment.
    4. Manual modification override.
    5. Delete all tweets.
    6. Quit.
    """)


# Open connection to firebase.
db = initialize_firestore()

# Authenticate with twitter.
# Courtesy of https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/twitter-data-in-python/
# Authors: Martha Morrissey, Leah Wasser, Carson Farmer
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

while True:

    display_table()
    choice = input("Please enter a number: ")

    if choice == '1':
        key_words = input("Enter key word to search: ")
        start_date = input("Enter the start date of the search in the format of YYYY-MM-DD: ")
        items = input("Define the number of tweets to retrieve: ")
        update_db(db, key_words, start_date, int(items))

    elif choice == '2':
        display_db(db)

    elif choice == '3':
        calculate_sentiment(db)

    elif choice == '4':
        screen_name = input("Enter the name of the user whose tweet will be modified: ")
        tweet = input("New tweet: ")
        modify_db(db, screen_name, tweet)

    elif choice == '5':
        delete_db(db)

    elif choice == '6':
        break

    else:
        print("Please input a valid option.")
        continue