# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
import re as re
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('Agg')
import time
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable

# http://metrics-api.dimensions.ai/doi/

# Import preprocessed data
df = pd.read_csv('/mnt/c/DATAscratch/SIPG/ICESpublications.csv')

#df["Series"].unique()
#df2 = df["External DOI"].dropna()

#'https://doi.org/'

#df
#count_wg = df.groupby([wg])[wg].count().sort_values(ascending=False)

#'Published under the auspices of the following ICES Steering Group or Committee'

urlstr = 'http://metrics-api.dimensions.ai/doi/'+'10.1121/1.2710741'

ids = json.loads(requests.get(urlstr).content)

print('\nGet dimensions information:')
data = pd.DataFrame()

for i, _df in enumerate(df.id):
    # pause(2s)
    doi_raw = df.loc[i]["External DOI"]
    # print(urlstr2)
    if not pd.isna(doi_raw):
        try:
            # doi = doi_raw.split('https://doi.org/')[1].split('\']')[0]
            doi = doi_raw[22:-2]
            urlstr = 'http://metrics-api.dimensions.ai/doi/'+doi
            print(urlstr)
            # print(doi_raw)
            ids = json.loads(requests.get(urlstr).content)
            # urlstr='https://www.doi.org/10.3389/fmars.2018.00072'
            # ids = json.loads(requests.get(urlstr).content)
            # https://www.doi.org/10.3389/fmars.2018.00072

            # _df = df.from_dict(ids.items()).transpose()
            _data = pd.DataFrame.from_dict(ids, orient='index').transpose()
            _data['id'] = _df
            data = pd.concat([data, _data], ignore_index = True)
            time.sleep(1)
        except:
            print(str(i)+'Failed'+doi_raw)
            # ids = json.loads(requests.get(urlstr).content)
    #articles_j.extend(ids)
data.to_pickle('/mnt/c/DATAscratch/SIPG/ICESdimensions.pk')
