[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">

<h3 align="center">EntiTweet</h3>

  <p align="center">
    A web app for creating Twitter co-occurence networks using Spacy and Flair
    <br />
    <a href="https://entitweet-app.onrender.com/"><strong>Try it out!</strong></a>
    <br />
  </p>
</div>

# EntiTweet

EntiTweet is a Flask web app aimed at creating visualizations of Twitter "co-ocurrence networks" with named entities. It collects the most recent tweets related to a user-inputted search query, and utilizes the user's choice of SpaCy or Flair to perform Named Entity Recognition (NER) on each tweet. These entities are collected and added as nodes to a graph using the NetworkX package. Edges are then added to the graph; two nodes are connected by an edge if they co-ocurr. The criteria for co-ocurrence is that both entities must be present in the same tweet. The graph is then rendered using the PyVis package. 

Please visit the [app page](https://entitweet-app.onrender.com/) and try it for yourself! Note that the live version on render.com doesn't include the Flair functionality, as the hosting site didn't have enough memory for the Flair model. 

## Running the App Locally

First, clone the repository.

```bash
git clone https://github.com/sumeetk321/EntiTweet.git
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies. These are outlined in ```requirements.txt```. Simply run ```app.py``` or run the following command to start the server:

```bash
flask run
```

Most likely you'll have to visit ```127.0.0.1:5000``` on your browser to access the server. Happy network analyzing!


## Usage

On the website, simply enter the search query, the number of tweets you'd like to use to create the network. Let's input **Stephen Curry** as our Twitter query, and let's use the last **30** tweets with this query to generate the network:

<img src="https://user-images.githubusercontent.com/18608410/211944312-cb2d5d72-6938-46fb-b855-0a3a4d9faa08.png">

After pressing Submit, here is our result:

<img src="https://user-images.githubusercontent.com/18608410/211944946-8bd321a4-a33d-44bf-bc3e-5016e236d9d9.png">

Enjoy!

## Contributing

I welcome pull requests! 

## License

Distributed under the MIT License. See ```LICENSE.txt``` for more information.

## Contact

Sumeet Kulkarni - sumeetk2@illinois.edu

Project Link: [https://github.com/sumeetk321/EntiTweet](https://github.com/sumeetk321/EntiTweet)

[contributors-shield]: https://img.shields.io/github/contributors/sumeetk321/EntiTweet.svg?style=for-the-badge
[contributors-url]: https://github.com/sumeetk321/EntiTweet/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sumeetk321/EntiTweet.svg?style=for-the-badge
[forks-url]: https://github.com/sumeetk321/EntiTweet/network/members
[stars-shield]: https://img.shields.io/github/stars/sumeetk321/EntiTweet.svg?style=for-the-badge
[stars-url]: https://github.com/sumeetk321/EntiTweet/stargazers
[issues-shield]: https://img.shields.io/github/issues/sumeetk321/EntiTweet.svg?style=for-the-badge
[issues-url]: https://github.com/sumeetk321/EntiTweet/issues
[license-shield]: https://img.shields.io/github/license/sumeetk321/EntiTweet.svg?style=for-the-badge
[license-url]: https://github.com/sumeetk321/EntiTweet/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/sumeet-kulkarni-798181172/
