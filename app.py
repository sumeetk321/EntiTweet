from flask import Flask, render_template, request
from pydantic import constr
import tweepy
import pandas as pd
import os
from dotenv import load_dotenv
import spacy
from pyvis.network import Network
import networkx as nx

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
def on_submit():
    G.clear()
    if request.method == "POST":
        search_query = request.form['query']
        max_num = request.form['max_num']
        #print(search_query)
        tweets_list = scrape_tweets(search_query, max_num)
        construct_graph(search_query, tweets_list)
        return render_template('graph.html')
    else:
        return render_template('index.html')

def scrape_tweets(search_query, count):
    response = client.search_recent_tweets(search_query, max_results = count)
    
    tweets = response.data
    tweets_list = []
    for tweet in tweets:
        tweets_list.append(tweet.text)
    return tweets_list

def construct_graph(search_ent, tweets_list):
    nt = Network()
    for tweet_text in tweets_list:
        spacy_ner = NER(tweet_text)
        ents = [(e.text, e.start, e.end, e.label_) for e in spacy_ner.ents]
        for i in range(len(ents)):
            G.add_edge(search_ent, ents[i][0])
            for j in range(i+1, len(ents)):
                G.add_edge(ents[i][0], ents[j][0])
    nt.from_nx(G)
    nt.show('templates/graph.html')
    
if __name__ == '__main__':
    app.run(debug=True)