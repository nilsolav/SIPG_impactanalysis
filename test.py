# -*- coding: utf-8 -*-



    
# See the number of articles
len(full_articles)

# View the metadata for the first article in JSON format
full_articles[0]

# Create a dataframe from the JSON formatted data
df = pd.DataFrame(full_articles)

# Some resources for the next steps
# https://dev.to/dmitryzub/scrape-google-scholar-with-python-32oh
# https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/

"""## Split out custom metadata fields
If a field does not exist for an item, it will show NaN (i.e. null).
1. Create a dataframe of custom metadata fields
2. Merge that dataframe with the original metadata dataframe
3. Save to an excel file
"""

# The custom fields are all contained within one column called 'custom_fields'. Flatten that column and associate the values
# with the proper article id
custom = pd.json_normalize(
    full_articles, 
    record_path =['custom_fields'], 
    meta=['id']
)
#This reshapes the data so that metadata field names are columns and each row is an id.
custom = custom.pivot(index="id", columns="name", values="value")

#Merge the dataframes so that all the custom fields are visible along with all the other metadata
custom_split_out = df.merge(custom, how='inner', on='id')

"""# Download Metadata

## If you are running this in Google Colab
"""

#When you run this cell it will ask you to authenticate so that you can create files to download
from google.colab import drive
drive.mount('/drive')

from google.colab import files
custom_split_out.to_csv('public-metadata-'+str(datetime.datetime.now().strftime("%Y-%m-%d"))+'.csv',encoding='utf-8') #create the CSV
files.download('public-metadata-'+str(datetime.datetime.now().strftime("%Y-%m-%d"))+'.csv') #download to your computer

"""## If you are running this locally
That is you downloaded the Jupyter Notebook
"""

#Save a file of all the metadata with the custom fields split out.
save_file = custom_split_out.to_excel("metadata-custom-fields-split-out.xlsx")
