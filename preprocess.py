# -*- coding: utf-8 -*-
import pandas as pd
import re as re
import json

# TODOS: 
# Altmetrics counts
# Citation counts (ICES publication)

# Read downloaded data
articles = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESarticles.pk')
full_articles = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESfull_articles.pk')
custom = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICEScustom.pk')
stats = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESstats.pk')
stats.index = stats.index.astype("int64")
dimensions = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESdimensions.pk')

# Merge the dataframes so that all the custom fields are visible along with all
# the other metadata
# Use left join on articles 
df = articles
df = df.merge(custom, how='left', on='id')
df = df.merge(full_articles, how='left', on='id')
df = df.merge(stats, how='left', on='id')
df = df.merge(dimensions, how='left', on='id')

print(len(articles))
print(len(custom))
print(len(full_articles))
print(len(stats))


# Remove HTML and new line characters in fields
def remove_tags(string):
    if isinstance(string, str):
        string = string.replace("\n", " ")
        result = re.sub('<.*?>', '', string)
    else:
        result = string
    return result


for f in df.columns:
    df[f] = df[f].apply(lambda cw: remove_tags(cw))

# Expand timeline
timeline = pd.DataFrame()
timeline_raw = df['timeline_y']
for i, _date in enumerate(timeline_raw):
    #ids = json.loads(df['timeline_y'].iloc[i].replace("'", "\""))
    #ids = json.loads(_date.replace("'", "\""))
    ids = _date
    _timeline = pd.DataFrame.from_dict(ids, orient='index').transpose()
    _timeline['id'] = df['id'][i]
    timeline = pd.concat([timeline, _timeline], ignore_index = True)
df = df.merge(timeline, how='left', on='id')


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

df.to_csv('/mnt/c/DATAscratch/SIPG/ICESpublications.csv')


# Word cloud on abstracts

# Altmetric API
# https://api.altmetric.com/v1/doi/10.1038/480426a

# Some resources for the next steps
# https://dev.to/dmitryzub/scrape-google-scholar-with-python-32oh
# https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/
