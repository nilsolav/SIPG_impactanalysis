# -*- coding: utf-8 -*-
import pandas as pd
import re as re

# Read downloaded data
articles = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESarticles.pk')
full_articles = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESfull_articles.pk')
custom = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICEScustom.pk')

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


# Remove HTML and new line characters in fields
def remove_tags(string):
    if isinstance(string, str):
        string = string.replace("\n", " ")
        result = re.sub('<.*?>', '', string)
    else:
        result = string
    return result

for f in df.columns:
    df[f] = df[f].apply(lambda cw : remove_tags(cw))

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

# Add to the df:

# Views
# Downloads
# Altmetrics counts
# Citation counts
# WG
# Publication type
# SG


# Word cloud on abstracts

# Altmetric API
# https://api.altmetric.com/v1/doi/10.1038/480426a

# Some resources for the next steps
# https://dev.to/dmitryzub/scrape-google-scholar-with-python-32oh
# https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/
