# EntiTweet

EntiTweet is a Flask web app aimed at creating visualizations of Twitter co-ocurrence networks with named entities. It works by collecting the most recent tweets related to a user-inputted search query, and using SpaCy to perform Named Entity Recognition (NER) on each tweet. These entities are collected and added as nodes to a graph using the NetworkX package. Edges are then added to the graph; two nodes are connected by an edge if they co-ocurr. The criteria for co-ocurrence is that both entities must be present in the same tweet. The graph is then rendered using the PyVis package. 

Please visit the app page and try it for yourself!

* App page: [https://entitweet.herokuapp.com/](https://entitweet.herokuapp.com/)

## Running the App Locally

First, clone the repository.

```bash
git clone https://github.com/sumeetk321/EntiTweet.git
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies. These are outlined in ```app.py```. If running on an IDE, simply run ```app.py``` and the Flask server should start on its own. You can also run the following command to start the server:

```bash
flask run
```

Most likely you'll have to visit ```127.0.0.1:5000``` on your browser to access the server. Happy network analyzing!



## Usage

On the website, simply enter the search query and the number of tweets you'd like to use to create the network. You will be led to a webpage with the interactive rendered graph.

## Contributing
I welcome pull requests! 

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)