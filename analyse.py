import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('Agg')

# Import preprocessed data
df = pd.read_csv('/mnt/c/DATAscratch/SIPG/ICESpublications.csv')

# Count by expert groupby
wg = 'Published under the auspices of the following ICES Expert Group or Strategic Initiative'
count_wg = df.groupby([wg])[wg].count().sort_values(ascending=False)
print(count_wg[0:20])
count_wg[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESpublications_WG.png')

# Download by expert groupby
downloads_wg = df.groupby([wg])['downloads'].sum().sort_values(ascending=False)
print(downloads_wg[0:20])
downloads_wg[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESdownloads_WG.png')

# Download by series 
downloads_series = df.groupby(['Series'])['downloads'].sum().sort_values(
    ascending=False)
print(downloads_series[0:20])
downloads_series[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESdownloads_pubtype.png')

# Count by series 
downloads_series = df.groupby(['Series'])['Series'].count().sort_values(
    ascending=False)
print(downloads_series[0:20])
downloads_series[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESdownloads_series.png')

# Mean download by series 
mean_downloads_series = df.groupby(['Series'])['downloads'].mean().sort_values(
    ascending=False)
print(mean_downloads_series[0:20])
downloads_series[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESmean_downloads_series.png')
