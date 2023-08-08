# -*- coding: utf-8 -*-
import pandas as pd
import re as re

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
    if (type(_date) is dict):
        ids = _date
        _timeline = pd.DataFrame.from_dict(ids, orient='index').transpose()
        _timeline['id'] = df['id'][i]
        timeline = pd.concat([timeline, _timeline], ignore_index = True)
df = df.merge(timeline, how='left', on='id')

# Extract the individual files
files = pd.DataFrame([], columns=['id', 'file'])
for i, _files in enumerate(df['files']):
    # urlstr = 'https://ices-library.figshare.com/ndownloader/files/'+str(ind)
    if isinstance(_files, list):
        __files = pd.DataFrame.from_dict(_files)
        #__files = pd.DataFrame([_files])

        if len(__files) > 0:
            __files['id_file'] = __files['id']
            __files['id'] = df['id'][i]
            # https://github.com/pandas-dev/pandas/issues/46662
            __files['is_link_only'] = __files['is_link_only'].astype("boolean")
            files = pd.concat([files, __files], ignore_index = True)

df.to_csv('/mnt/c/DATAscratch/SIPG/ICESpublications.csv')
df.to_pickle('/mnt/c/DATAscratch/SIPG/ICESpublicaitons.pk')
files.to_pickle('/mnt/c/DATAscratch/SIPG/ICESfiles.pk')
