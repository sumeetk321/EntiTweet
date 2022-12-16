"""This file handles all requests and computations for EntiTweet"""
import os
import re
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
import tweepy
from dotenv import load_dotenv
import spacy
from pyvis.network import Network
import networkx as nx
from fuzzywuzzy import fuzz
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
matplotlib.use('Agg')

RATIO_CONSTANT = 85
NUM_TWEETS_MAX = 100

load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')

client = tweepy.Client(bearer_token)

NER = spacy.load("en_core_web_sm")

G = nx.Graph()

splitter = SegtokSentenceSplitter()
tagger = SequenceTagger.load('ner')

app = Flask(__name__)

@app.route('/')
def index():
    """Returns the static homepage"""
    return render_template('index.html')

@app.route('/graph', methods =['GET', 'POST'])
def on_submit():
    """Use submitted form data to begin construction of graph"""
    G.clear()
    if request.method == "POST":
        search_query = request.form['query']
        num_tweets = request.form['num_tweets']
        flair_or_spacy = request.form['dropdown']
        if len(search_query) == 0 or int(num_tweets) > NUM_TWEETS_MAX:
            return render_template('index.html')
        tweets_list = scrape_tweets(search_query, num_tweets)
        data_list = construct_graph(search_query, tweets_list, flair_or_spacy)
        nx.draw_networkx(G, pos=nx.fruchterman_reingold_layout(G), node_size=50, font_size=5,
            edge_color='#E84A27', width=0.5, with_labels=True) #Go Illini!
        plt.savefig('templates/graph.png', dpi=500)
        return render_template('graph.html', nodes=data_list[0], edges=data_list[1],
            heading=data_list[2], height=data_list[3], width=data_list[4], options=data_list[5])
    return render_template('index.html')

def scrape_tweets(search_query, count):
    """Uses tweepy Client to gather a list of processed tweet text data"""
    response = client.search_recent_tweets(search_query, max_results = count)
    tweets = response.data
    tweets_list = []
    for tweet in tweets:
        tweets_list.append(preprocess(tweet.text))
    return tweets_list

def construct_graph(search_ent, tweets_list, flair_or_spacy):
    """Construct a graph using PyVis. Add edges one at a time using entities
        found by SpaCy NER. Export the graph to an html file"""
    if flair_or_spacy=="spacy":
        return construct_spacy_graph(search_ent, tweets_list)
    return construct_flair_graph(search_ent, tweets_list)


def construct_spacy_graph(search_ent, tweets_list):
    """Constructs the graph using Spacy as the main NER library"""
    network = Network()
    for tweet_text in tweets_list:
        spacy_ner = NER(tweet_text)
        ents = [(e.text, e.start, e.end, e.label_) for e in spacy_ner.ents]
        for i, _ in enumerate(ents):
            if fuzz.ratio(search_ent, ents[i][0]) > RATIO_CONSTANT:
                continue
            G.add_edge(search_ent, ents[i][0])
            for j in range(i+1, len(ents)):
                if fuzz.ratio(search_ent, ents[j][0]) > RATIO_CONSTANT:
                    continue
                G.add_edge(ents[i][0], ents[j][0])
    network.from_nx(G)
    return get_data_list(network)

def construct_flair_graph(search_ent, tweets_list):
    """Constructs the graph using Flair as the main NER library"""
    network = Network()
    for tweet_text in tweets_list:
        sentences = splitter.split(tweet_text)
        tagger.predict(sentences)
        for sentence in sentences:
            spans = sentence.get_spans('ner')
            for i, _ in enumerate(spans):
                entity = spans[i]
                # print entity text, start_position and end_position
                if fuzz.ratio(search_ent, entity.text) > RATIO_CONSTANT:
                    continue
                G.add_edge(search_ent, entity.text)

                for j in range(i+1, len(spans)):
                    if fuzz.ratio(search_ent, spans[j].text) > RATIO_CONSTANT:
                        continue
                    G.add_edge(entity.text, spans[j].text)
    network.from_nx(G)
    return get_data_list(network)


def get_data_list(network):
    """Returns network info"""
    nodes, edges, heading, height, width, options = network.get_network_data()
    data_list = [nodes, edges, heading, height, width, options]
    return data_list

def preprocess(tweet):
    """Processes tweets; removes retweet "RT" strings, URLs, hashtags, and single numeric digits"""
    processed_tweet = re.sub(r'^RT[\s]+', '', tweet)
    processed_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', processed_tweet)
    processed_tweet = re.sub(r'#', '', processed_tweet)
    processed_tweet = re.sub(r'[0-9]', '', processed_tweet)
    return processed_tweet

@app.route('/download')
def download_graph():
    """Sends graph file to user"""
    path = "templates/graph.png"
    return send_file(path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
