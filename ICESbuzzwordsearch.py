import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

files = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESfiles.pk')
df = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESpublications.pk')

# find subset of files based on decade
dec = pd.date_range('1889-12-31',
                    '2019-12-31',
                    freq = '1Y')

ecosystem = []
Y = []
r1 = []
r2 = []
r3 = []
r4 = []
N = []

for _dec in dec:
    # Initalize data frame
    data = pd.DataFrame([], columns=['id_file', 'keywords'])
    # subset
    _df = (pd.to_datetime(df['publisherPublication']) > _dec)
    _df2 = (pd.to_datetime(df['publisherPublication']) < 
            (_dec + pd.offsets.DateOffset(years=1)))
    ind = _df & _df2
    
    # Get the IDs for this year
    _ind = set(df['id'][ind])
    _files = files.loc[files["id"].isin(_ind), :]
    # Get files from this year
    for __files in _files["id_file"]:
        pkfile = '/mnt/c/DATAscratch/SIPG/pdf/'+str(int(__files))+'.pdf.pk'
        if os.path.exists(pkfile):
            # Read file            
            _data = pd.read_pickle(pkfile)
            data = pd.concat([data, _data], ignore_index = True)

    # Create wordcloud for this decade
    text = ' '.join(data['keywords'])
    if len(data) > 0:
        Y.append(_dec)
        N.append(text.lower().count(' '))
        r1.append(text.lower().count('ecosystem '))
        r2.append(text.lower().count('integrated ecosystem assessment'))
        r3.append(text.lower().count('ecosystem based'))
        r4.append(text.lower().count('multi species'))


df = pd.DataFrame(list(zip(N, r1, r2, r3, r4)), index = Y,
                  columns =['N', 'ecosystem', 'IEA','ecosystem based','multi species'])

df2 = pd.DataFrame()
df2['ecosystem'] = df['ecosystem']/df['N']
df2['Integrated Ecosystem Assessment'] = df['IEA']/df['N']
df2['ecosystem based'] = df['ecosystem based']/df['N']
df2['multi species'] = df['multi species']/df['N']

df2.plot()
plt.show()
