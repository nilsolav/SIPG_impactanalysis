import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('/mnt/c/DATAscratch/SIPG/ICESpublications.csv')

# Count by expert groupby
col = 'Published under the auspices of the following ICES Expert Group or Strategic Initiative'
df2 = df.groupby([col])[col].count()
count_wg = df2.sort_values(ascending=False)
print(count_wg[0:20])
count_wg[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESpublications_WG.png')

# Download by expert groupby
col2 = 'downloads'
df2 = df.groupby([col])[col2].sum()
downloads_wg = df2.sort_values(ascending=False)
print(downloads_wg[0:20])
downloads_wg[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESdownloads_WG.png')

# Download by series 
col2 = 'Series'
df3 = df.groupby([col2])[col2].count()
downloads_series = df3.sort_values(ascending=False)
print(downloads_series[0:20])
downloads_series[0:20].plot.barh()
plt.savefig('/mnt/c/DATAscratch/SIPG/ICESdownloads_pubtype.png')
