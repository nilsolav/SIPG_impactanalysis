import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('Agg')
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable

# Some resources for the next steps
# https://dev.to/dmitryzub/scrape-google-scholar-with-python-32oh
# https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/


# Import preprocessed data
df = pd.read_csv('/mnt/c/DATAscratch/SIPG/ICESpublications.csv')

# total number of downloads
print(sum(df['downloads']))

# Count by expert groupby
wg = 'Published under the auspices of the following ICES Expert Group or Strategic Initiative'
count_wg = df.groupby([wg])[wg].count().sort_values(ascending=False)
print(count_wg[0:10])
count_wg[0:10].plot.barh().invert_yaxis()
plt.xlabel('Count by WG')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESpublications_WG.png')
plt.close()

# Download by expert groupby
downloads_wg = df.groupby([wg])['downloads'].sum().sort_values(ascending=False)
print(downloads_wg[0:10])
downloads_wg[0:10].plot.barh().invert_yaxis()
plt.xlabel('Download by WG')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESdownloads_WG.png')
plt.close()

# Citations by expert groupby
times_cited_wg = df.groupby([wg])['times_cited'].sum().sort_values(ascending=False)
print(times_cited_wg[0:20])
times_cited_wg[0:10].plot.barh().invert_yaxis()
plt.xlabel('Citations by WG')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICEScitations_WG.png')
plt.close()

# list(df.columns)
# Recent_citations by wg
recent_citations_wg = df.groupby([wg])['recent_citations'].sum().sort_values(ascending=False)
print(recent_citations_wg[0:10])
downloads_wg[0:10].plot.barh().invert_yaxis()
plt.xlabel('Recent Citations by WG')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESrecent_citations_WG.png')
plt.close()

# Average download by expert groupby
mean_downloads_wg = df.groupby([wg])['downloads'].mean().sort_values(ascending=False)
print(mean_downloads_wg[0:10])
mean_downloads_wg[0:10].plot.barh().invert_yaxis()
plt.xlabel('Average download by WG')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESmean_downloads_WG.png')
plt.close()

# Relative_citation_ratio
relative_citation_ratio = df.groupby([wg])['relative_citation_ratio'].mean().sort_values(ascending=False)
print(relative_citation_ratio[0:10])
mean_downloads_wg[0:10].plot.barh().invert_yaxis()
plt.xlabel('Relative citation ratio')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESmean_relative_citaion_ratio_WG.png')
plt.close()

# Download by series 
downloads_series = df.groupby(['Series'])['downloads'].sum().sort_values(
    ascending=False)
print(downloads_series[0:10])
downloads_series[0:10].plot.barh().invert_yaxis()
make_axes_area_auto_adjustable(plt.gca())
plt.xlabel('Download by series')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESdownloads_pubtype.png')
plt.close()
sum(downloads_series)
# Count by series 
downloads_series = df.groupby(['Series'])['Series'].count().sort_values(
    ascending=False)
print(downloads_series[0:20])
downloads_series[0:10].plot.barh().invert_yaxis()
fig = plt.gcf()
fig.set_size_inches(15, 5)
make_axes_area_auto_adjustable(plt.gca())
plt.xlabel('Count by series')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICEScount_pubtype.png')
plt.close()

# Mean download by series 
mean_downloads_series = df.groupby(['Series'])['downloads'].mean().sort_values(
    ascending=False)
print(mean_downloads_series[0:10])
mean_downloads_series[0:10].plot.barh().invert_yaxis()
fig = plt.gcf()
fig.set_size_inches(15, 5)
make_axes_area_auto_adjustable(plt.gca())
plt.xlabel('Mean download by series')
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESmean_downloads_series.png')
plt.close()


# item by years
years = pd.to_datetime(df['publisherPublication'].dropna()).dt.year.astype(int)
ax = years.value_counts().sort_index().plot(kind='line')
ax.set_xticks(ticks=range(1890, 2030, 10))
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESmean_dates.png')
plt.close()
