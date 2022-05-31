import flask
from flask import Flask, render_template, request
from tweepy import OAuthHandler
from tweepy.streaming import Stream
import tweepy
import json
import pandas as pd
import csv
import re
import string
import os
import time
from dotenv import load_dotenv
import spacy
import numpy as np

load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')

client = tweepy.Client(bearer_token)   

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods =['GET', 'POST'])
def onSubmit():
    if request.method == "POST":
        search_query = request.form['query']
        max_num = request.form['max_num']
        print(search_query)
    else:
        return render_template('index.html')

def scrape_tweets(search_query, count):
    response = client.search_recent_tweets(search_query, max_results = count)
    
    tweets = response.data
    df = pd.DataFrame(columns = ['tweet_id', 'tweet_text'])
    for tweet in tweets:
        df = df.append({'tweet_id':tweet.id, 'tweet_text': tweet.text}, ignore_index=True)
    return df
    
if __name__ == '__main__':
    app.run(debug=True)