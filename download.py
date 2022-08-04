import json
import requests
import pandas as pd
from tqdm import tqdm

# Set variables
BASE_URL = "https://api.figshare.com/v2/"
INST_ID = "12" # I need  ICES code!
ITEMS = "3" # Needs to match the total number of items/10

# Gather basic metadata for all items (articles) from the Figshare articles API endpoint
articles_j = []
print('\nGet list of items:')
for i in tqdm(range(1, 5)): # Loop over 10 "pages", with 10 items per page
    urlstr = BASE_URL+"articles?institution="+INST_ID+\
        "&order=published_date&order_direction=desc&page_size="+\
        ITEMS+"0&page={}".format(i)
    ids = json.loads(requests.get(urlstr).content)
    articles_j.extend(ids)
articles = pd.DataFrame(articles_j)
articles = articles.set_index('id')

# Create a list of all the article ids
article_ids = articles.index

# For each id in the article id list, retrieve all the metadata for the article by visiting the Figshare article API endpoint 
# This may take a while- for example, 6,000 records takes about 1.5 hours
full_articles_j = []
print('\nGet detailed information for each item:')
for art_id in tqdm(article_ids):
    article_j = json.loads(requests.get(BASE_URL + "articles/{}".
                                      format(str(art_id))).content)
    full_articles_j.append(article_j)

full_articles = pd.DataFrame(full_articles_j)

# The custom fields are all contained within one column called 'custom_fields'. Flatten that column and associate the values
# with the proper article id
custom = pd.json_normalize(
    full_articles_j, 
    record_path =['custom_fields'], 
    meta=['id']
)
# This reshapes the data so that metadata field names are columns and each row is an id.
custom = custom.pivot(index="id", columns="name", values="value")

'''
# Flatten the files dictionary
files = pd.DataFrame()
for it in full_articles.files:
    try:
        files = files.append(it[0], ignore_index=True, sort=False)
    except:
        print('Failed')
 Set Id as index
files = files.set_index('id')
'''

# Merge the dataframes so that all the custom fields are visible along with all the other metadata
df = articles
df = df.merge(custom, how='left', on='id')
df = df.merge(full_articles, how='inner', on='id')
'''
len(df)
len(full_articles)
len(custom)
'''

# Save data to pickle file (I tried to use the to_csv but it failed since
# there are HTML tags and \n codes in the text that causes the files to
# be break new lines. Probably an easy fix.

df.to_pickle('/mnt/c/DATAscratch/SIPG/ICESpublications.pk')
