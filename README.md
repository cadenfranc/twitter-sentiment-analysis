# Overview
This program was made to calculate the sentiment of tweets gathered using the tweepy module. Data is gathered from twitter in real time and is stored into a Firestore collection for analysis.

My goal in the development of this project was to learn more in respect to storing, modifying, and retrieving data from a cloud database, and to gain familiarity with the tweepy module.

[Software Demo Video](https://youtu.be/iBcDAtkSl8Y)

# Cloud Database

**COLLECTION**
* Twitter Data Collection (twitter_data)

    **DOCUMENTS**

    * Firestore Auto Generated ID
        
        **FIELDS**
        * user_name : STRING
        * tweet : STRING


# Development Environment
* firebase-admin : Connect to firebase.
* tweepy : Gather tweets from twitter.
* TextBlob : Analyze sentiment.
* re : Formatting data for enhanced readibility.
* Python 3.8.7
* Visual Studio Code

# Useful Websites
* [Firebase Documentation](https://firebase.google.com/docs)
* [Automate Getting Twitter Data in Python Using Tweepy](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/twitter-data-in-python/)

# Future Work
* Implementation of a Recurrent Neural Network (RNN) using TensorFlow for more accurate, customizeable sentiment analysis.
* Advanced error and exception handling to avoid unreadable inputs or premature termination of the program.
* Development of a user friendly interface.