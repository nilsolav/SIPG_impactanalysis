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
                    freq = '10Y')

for _dec in dec:
    # Initalize data frame
    data = pd.DataFrame([], columns=['id_file', 'keywords'])
    # subset
    _df = (pd.to_datetime(df['publisherPublication']) > _dec)
    _df2 = (pd.to_datetime(df['publisherPublication']) < 
            (_dec + pd.offsets.DateOffset(years=10)))
    ind = _df & _df2
    
    # Get the IDs for this decade
    _ind = set(df['id'][ind])
    _files = files.loc[files["id"].isin(_ind), :]
    # Get files from this decade
    for __files in _files["id_file"]:
        pkfile = '/mnt/c/DATAscratch/SIPG/pdf/'+str(int(__files))+'.pdf.pk'
        if os.path.exists(pkfile):
            # Read file            
            _data = pd.read_pickle(pkfile)
            data = pd.concat([data, _data], ignore_index = True)

    # Create wordcloud for this decade
    wfile = '/mnt/c/DATAscratch/SIPG/ICESwordcloud' + str(_dec.year)+'.png'
    text = ' '.join(data['keywords'])
    if len(data) > 0:
        wordcloud = WordCloud(width = 800, height = 800, 
                              background_color ='white', 
                              min_font_size = 10).generate(text)
        
        # plot the WordCloud image                        
        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 
        plt.savefig(wfile)
        plt.close()
