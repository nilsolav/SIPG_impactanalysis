import json
import requests
import pandas as pd
#from tqdm import tqdm

# Set variables
BASE_URL = "https://api.figshare.com/v2/"
ITEMS = "1" # Needs to match the total number of items/10

# Gather basic metadata for all items (articles) from the Figshare articles API endpoint
res_all = []
for INST_ID in range(950, 1000):
    urlstr = BASE_URL+"articles?institution="+str(INST_ID)+\
        "&order=published_date&order_direction=desc&page_size="+\
        ITEMS+"0&page=1"
    ids = json.loads(requests.get(urlstr).content)
    # Search for ICES
    if len(ids) > 0: # is not None:
        nils = ids[0]['url_public_html']
        print(nils)
        res_all.append([INST_ID, nils])



