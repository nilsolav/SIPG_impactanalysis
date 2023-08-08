# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd

# This script downloads dimensions data
# http://metrics-api.dimensions.ai/doi/

# Import custom fields where external doi is present
df = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICEScustom.pk')

# Extract data from dimentions database
data = pd.DataFrame()
for i, _df in enumerate(df.index):
    doi_raw = df.iloc[i]["External DOI"]
    if not (pd.isna(doi_raw) or len(doi_raw)<1):
        try:
            try:
                doi = doi_raw[0].split('https://www.doi.org/')[1]
                urlstr = 'http://metrics-api.dimensions.ai/doi/'+doi
                print(urlstr)
                ids = json.loads(requests.get(urlstr).content)
            except:
                doi = doi_raw[0].split('https://doi.org/')[1]
                urlstr = 'http://metrics-api.dimensions.ai/doi/'+doi
                print(urlstr)
                ids = json.loads(requests.get(urlstr).content)

            _data = pd.DataFrame.from_dict(ids, orient='index').transpose()
            _data['id'] = _df
            data = pd.concat([data, _data], ignore_index = True)
            print(str(i)+' Success '+doi_raw[0])
        except:
            print(str(i)+' Failed '+str(doi_raw))

# save to file
data.to_pickle('/mnt/c/DATAscratch/SIPG/ICESdimensions.pk')
