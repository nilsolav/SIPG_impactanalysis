import pandas as pd
import datetime

# Import preprocessed data
df = pd.read_csv('/mnt/c/DATAscratch/SIPG/ICESpublications.csv')
list(df.columns)

# Pick time interval
df['publisherPublication'] = pd.to_datetime(df['publisherPublication'])
ind = (df['publisherPublication'] > datetime.datetime(2001, 1, 1)) & (
    df['publisherPublication'] > datetime.datetime(2022, 1, 1))
df1 = df[ind]
df1 = df
# Search for names
names = ['Handegard'] # need to refect what you are searching for
hits = [df1['Contributors (Authors)'].str.find(name) > 0 for name in names]
hit = hits[0]
for _hits in hits:
    hit = hit | _hits

# List results
results = df1[hit][['Contributors (Authors)', 'title_x', 'publisherPublication', 'Series', 'url_public_html_y']]

results.to_csv('/mnt/c/DATAscratch/SIPG/ICESauthoredpublications.csv', sep = ';')
