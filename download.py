import json
import requests
import pandas as pd
from tqdm import tqdm

# Set variables
BASE_URL = "https://api.figshare.com/v2/"
INST_ID = "12" # I need  ICES code!
ITEMS = "10" # Needs to match the total number of items/10

# Gather basic metadata for all items (articles) from the Figshare articles API endpoint
articles = []
print('\nGet list of items:')
for i in tqdm(range(1, 10)): # Loop over 10 "pages", with 10 items per page
    str = BASE_URL+"articles?institution="+INST_ID+"&order=published_date&order_direction=desc&page_size="+ITEMS+"0&page={}".format(i)
    ids = json.loads(requests.get(str).content)
    articles.extend(ids)

# Create a list of all the article ids
article_ids = [item['id'] for item in articles]

# For each id in the article id list, retrieve all the metadata for the article by visiting the Figshare article API endpoint 
# This may take a while- for example, 6,000 records takes about 1.5 hours
full_articles = []
print('\nGet detailed information for each item:')
for art_id in tqdm(article_ids):
    article = json.loads(requests.get(BASE_URL + "articles/{}".
                                      format(art_id)).content)
    full_articles.append(article)

df = pd.DataFrame(full_articles)

# Save metadata to file
df.to_json('ICESpublications.json')
