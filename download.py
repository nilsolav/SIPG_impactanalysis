import json
import requests
import pandas as pd

# Set variables

BASE_URL = "https://api.figshare.com/v2/"
INST_ID = "658" #  Need ICES code

# Gather basic metadata for all items (articles) from the Figshare articles API endpoint
articles = []
for i in range(1,10):
    ids = json.loads(requests.get(BASE_URL + "articles?institution="+INST_ID+"&page_size=1000&page={}".format(i)).content)
    articles.extend(ids)

# See the number of articles
len(articles)

# Create a list of all the article ids
article_ids = [item['id'] for item in articles]

# For each id in the article id list, retrieve all the metadata for the article by visiting the Figshare article API endpoint 
# This may take a while- for example, 6,000 records takes about 1.5 hours
full_articles = []
for art_id in article_ids:
    article = json.loads(requests.get(BASE_URL + "articles/{}".format(art_id)).content)
    full_articles.append(article)
# Store the result
