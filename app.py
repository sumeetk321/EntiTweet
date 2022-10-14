from flask import Flask, render_template, request, send_file, url_for
import tweepy
import os
from dotenv import load_dotenv
import spacy
from pyvis.network import Network
import networkx as nx
import re
from fuzzywuzzy import fuzz
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    return render_template('index.html')

@app.route('/graph', methods =['GET', 'POST'])
#Use submitted form data to begin construction of graph.
def on_submit():
    G.clear()
    if request.method == "POST":
        search_query = request.form['query']
        num_tweets = request.form['num_tweets']
        flair_or_spacy = request.form['dropdown']
        if len(search_query) == 0 or int(num_tweets) > NUM_TWEETS_MAX:
           return render_template('index.html')
        tweets_list = scrape_tweets(search_query, num_tweets)
        data_list = construct_graph(search_query, tweets_list, flair_or_spacy)
        nx.draw_networkx(G, pos=nx.fruchterman_reingold_layout(G), node_size=50, font_size=5, edge_color='#E84A27', width=0.5, with_labels=True) #Go Illini!
        plt.savefig('templates/graph.png', dpi=500)
        return render_template('graph.html', nodes=data_list[0], edges=data_list[1], heading=data_list[2], height=data_list[3], width=data_list[4], options=data_list[5])
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
def construct_graph(search_ent, tweets_list, flair_or_spacy):
    nt = Network()
    if(flair_or_spacy=="spacy"):
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
    else:
        for tweet_text in tweets_list:

            sentences = splitter.split(tweet_text)
            tagger.predict(sentences)
            for sentence in sentences:
                spans = sentence.get_spans('ner')
                for i in range(len(spans)):
                    entity = spans[i]
                    # print entity text, start_position and end_position
                    if fuzz.ratio(search_ent, entity.text) > RATIO_CONSTANT:
                        continue
                    else:
                        G.add_edge(search_ent, entity.text)

                    for j in range(i+1, len(spans)):
                        if fuzz.ratio(search_ent, spans[j].text) > RATIO_CONSTANT:
                            continue
                        else:
                            G.add_edge(entity.text, spans[j].text)
        nt.from_nx(G)

    
    #nt.show('templates/graph.html')
    nodes, edges, heading, height, width, options = nt.get_network_data()
    
    data_list = [nodes, edges, heading, height, width, options]
    return data_list
    
#Process tweets; remove retweet "RT" strings, URLs, hashtags, and single numeric digits. 
def preprocess(tweet):
    processed_tweet = re.sub(r'^RT[\s]+', '', tweet)
    processed_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', processed_tweet)
    processed_tweet = re.sub(r'#', '', processed_tweet)
    processed_tweet = re.sub(r'[0-9]', '', processed_tweet)
    return processed_tweet

@app.route('/download')
def downloadGraph():
    path = "templates/graph.png"
    return send_file(path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)