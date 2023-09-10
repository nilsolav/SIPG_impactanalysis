import matplotlib.pyplot as plt
import pandas as pd
import os

files = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESfiles.pk')
df = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESpublications.pk')

# find subset of files based on decade
dec = pd.date_range('1889-12-31',
                    '2023-12-31',
                    freq = '1Y')

keywords = ['fisheries management',
            'integrated ecosystem assessment',
            'ecosystem based',
            'multi species',
            'recruitment',
            'north sea',
            'baltic',
            'norwegian sea',
            'aquaculture',
            'mariculture',
            'cod', 'herring', 'eel', 'mackerel', 'salmon',
            'hydrography','oceanography',
            'plankton']

dat = []
Y = []
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

    # Create text string for _dec
    text = ' '.join(data['keywords'])
    if len(data) == 0:
        text = ' '
    
    Y.append(_dec)
    N.append(text.lower().count(' '))

    cnt = []
    for _keywords in keywords:
        cnt.append(text.lower().count(_keywords))
    dat.append(cnt)

# Change to data frame
df = pd.DataFrame(dat, columns=keywords, index=Y)
df['N'] = pd.DataFrame(N, index=Y)
df2 = pd.DataFrame()
for _keywords in keywords:
    df2[_keywords] = df[_keywords]/df['N']

# Aquaculture in ICES?
f3 = df2[['mariculture', 'aquaculture']].plot()

# Areas?
f4 = df2[['north sea', 'baltic', 'norwegian sea']].plot()

f5 = df2[['fisheries management',
          'integrated ecosystem assessment',
          'ecosystem based',
          'multi species']].plot()

f6 = df2[['cod', 'herring', 'eel', 'mackerel', 'salmon']].plot()

f7 = df2[['hydrography', 'oceanography', 'plankton']].plot()

plt.show()
