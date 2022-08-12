import requests
import pandas as pd
from tqdm import tqdm

# File ID different than item ID:
# https://ices-library.figshare.com/ndownloader/files/36478023
# https://ices-library.figshare.com/articles/report/Working_Group_on_International_Deep_Pelagic_Ecosystem_Surveys_WGIDEEPS_/20401581

articles = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESarticles.pk')
full_articles = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESfull_articles.pk')
custom = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICEScustom.pk')
stats = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESstats.pk')


files = pd.DataFrame([], columns=['id', 'file'])
for i, _files in tqdm(enumerate(full_articles['files'][9:10])):
    # urlstr = 'https://ices-library.figshare.com/ndownloader/files/'+str(ind)
    if len(_files) > 0:
        for _file in _files:
            # Download file
            url = _file['download_url']
            fname = '/mnt/c/DATAscratch/SIPG/pdf/'+str(_file['id'])+'.pdf'
            r = requests.get(url)
            open(fname , 'wb').write(r.content)
            # Save metadata
            files_i = pd.DataFrame([[full_articles['id'][i],_file['id']]],
                                   columns=['id', 'file'])
            files = pd.concat([files, files_i])

articles.to_pickle('/mnt/c/DATAscratch/SIPG/ICESfiles.pk')

