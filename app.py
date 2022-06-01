from flask import Flask, render_template, request
import tweepy
import os
from dotenv import load_dotenv
import spacy
from pyvis.network import Network
import networkx as nx
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

RATIO_CONSTANT = 85

load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')

client = tweepy.Client(bearer_token)

NER = spacy.load("en_core_web_sm")

G = nx.Graph()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph', methods =['GET', 'POST'])
#Use submitted form data to begin construction of graph.
def on_submit():
    G.clear()
    if request.method == "POST":
        search_query = request.form['query']
        max_num = request.form['max_num']
        tweets_list = scrape_tweets(search_query, max_num)
        construct_graph(search_query, tweets_list)
        return render_template('graph.html')
    else:
        return render_template('index.html')

#Use tweepy Client to gather a list of processed tweet text data. 
def scrape_tweets(search_query, count):
    response = client.search_recent_tweets(search_query, max_results = count)
    
    tweets = response.data
    tweets_list = []
    for tweet in tweets:
        tweets_list.append(preprocess(tweet.text))
    return tweets_list

#Construct a graph using PyVis. Add edges one at a time using entities found by SpaCy NER. Export the graph to an html file. 
def construct_graph(search_ent, tweets_list):
    nt = Network()
    for tweet_text in tweets_list:
        spacy_ner = NER(tweet_text)
        ents = [(e.text, e.start, e.end, e.label_) for e in spacy_ner.ents]
        for i in range(len(ents)):

            if fuzz.ratio(search_ent, ents[i][0]) > RATIO_CONSTANT:
                continue
            else:
                G.add_edge(search_ent, ents[i][0])

            for j in range(i+1, len(ents)):
                if fuzz.ratio(search_ent, ents[j][0]) > RATIO_CONSTANT:
                    continue
                else:
                    G.add_edge(ents[i][0], ents[j][0])
    nt.from_nx(G)
    nt.show('templates/graph.html')
    
#Process tweets; remove retweet "RT" strings, URLs, hashtags, and single numeric digits. 
def preprocess(tweet):
    processed_tweet = re.sub(r'^RT[\s]+', '', tweet)
    processed_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', processed_tweet)
    processed_tweet = re.sub(r'#', '', processed_tweet)
    processed_tweet = re.sub(r'[0-9]', '', processed_tweet)
    return processed_tweet




#if __name__ == '__main__':
 #   app.run(debug=True)