# SIPG_impactanalysis
Code to analyse ICES impact from SIPG

## download.py
Extract the records and stores in `ICESarticles.pk`, download metadata and store in `ICESfull_articles.pk`, flatten the ICES custom data and stores in `ICEScustom.pk`, and store the stats for the item in `ICESstats.pk`.

## dimensions.py
Read the preprocessed data from `ICEScustom.csv` and looks up the dimensions data base. Stores the data to `ICESdimensions.pk`.

## preprocess.py
Merge the data frames from `ICESarticles.pk`, `ICESfull_articles.pk`, `ICEScustom.pk`, `ICESstats.pk` and `ICESdimensions.pk`, removes HTML tags and new line characters, and stores the results to both `ICESpublications.csv` and `ICESpublicaitons.pk`. A separate list of pdf files are stored in `ICESfiles.pk` to be used by the full text analysis.

## analyse.py
Create figures and metadata counts from the `ICESpublications.csv`.

## download_papers.py
Reads the `ICESfiles.pk` and download the full text articles and store the pdfs in the `/pdf/` directory.

## ICESwordcloud.py
Extract the text from the pdf's.

## ICES wordcloud_2.py
Generate the word clouds based on the extracted texts.


