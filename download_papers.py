import requests
import pandas as pd
from tqdm import tqdm
from os.path import isfile

# File ID different than item ID:
# https://ices-library.figshare.com/ndownloader/files/36478023
# https://ices-library.figshare.com/articles/report/Working_Group_on_International_Deep_Pelagic_Ecosystem_Surveys_WGIDEEPS_/20401581

files = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESfiles.pk')

# Download file
for i, _file in tqdm(enumerate(files['id_file'])):
    url = files['download_url'][i]
    fname = '/mnt/c/DATAscratch/SIPG/pdf/'+str(int(_file))+'.pdf'
    # file exist?
    if not isfile(fname):
        try:
            r = requests.get(url)
            open(fname , 'wb').write(r.content)
            print(url+' : OK')
        except:
            print(url+' : Failed download')
    else:
        print(url+' : File already exists')
