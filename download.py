import json
import requests
import pandas as pd
from tqdm import tqdm

# Set variables
BASE_URL = "https://api.figshare.com/v2/"
INST_ID = "989" # The ICES code

ITEMS = "100" # Needs to match the total number of items

# 9001 posts

# Gather basic metadata for all items (articles) from the Figshare articles API endpoint
articles_j = []
print('\nGet list of items:')
for i in tqdm(range(1, 200)): # Loop over 53 "pages", with ITEMS items per page
    urlstr = BASE_URL+"articles?institution="+INST_ID+\
        "&order=published_date&order_direction=desc&page_size="+\
        ITEMS+"0&page={}".format(i)
    ids = json.loads(requests.get(urlstr).content)
    articles_j.extend(ids)

# If the number of items are larger than the number of items in the
# collection the articles_j list needs to be trimmed.
i = 0
for sub in articles_j:
    i = i + 1
    if sub == 'message':
        print(i)
        break
articles_j_sub = articles_j[0:(i-2)]    
articles = pd.DataFrame(articles_j_sub)
articles = articles.set_index('id')
articles.to_pickle('/mnt/c/DATAscratch/SIPG/ICESarticles.pk')

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
full_articles.to_pickle('/mnt/c/DATAscratch/SIPG/ICESfull_articles.pk')

# The custom fields are all contained within one column called 'custom_fields'. Flatten that column and associate the values
# with the proper article id
custom = pd.json_normalize(
    full_articles_j, 
    record_path =['custom_fields'], 
    meta=['id']
)
# This reshapes the data so that metadata field names are columns and each row is an id.
custom = custom.pivot(index="id", columns="name", values="value")
custom.to_pickle('/mnt/c/DATAscratch/SIPG/ICEScustom.pk')

# Get use stats
stats = pd.DataFrame()
for i, dfi in tqdm(enumerate(articles.index)):
    dat = {}
    dat.update({'id': dfi})
    for ctype in ['views', 'downloads', 'shares']:
        urlstr = 'https://stats.figshare.com/total/'+ctype+'/article/'+str(dfi)
        totals = json.loads(requests.get(urlstr).content)['totals']
        dat.update({ctype: totals})
    dat_df = pd.DataFrame([dat])
    stats = pd.concat([stats, dat_df], ignore_index=True)
print(stats.head())
stats = stats.set_index('id')
stats.index = stats.index.astype("int64")
stats.to_pickle('/mnt/c/DATAscratch/SIPG/ICESstats.pk')
