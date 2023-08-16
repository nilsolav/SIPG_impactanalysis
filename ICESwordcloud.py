import matplotlib.pyplot as plt
import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import re
import string
from wordcloud import WordCloud
import numpy as np
import tqdm
import os

# Count by expert groupby
# https://towardsdatascience.com/pdfs-to-word-cloud-in-3-steps-73ccbff6d835
# https://betterprogramming.pub/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f


def clean_text(text):
    # remove numbers
    text2 = re.sub(r'\\n', ' ', text)
    text_nonum = re.sub(r'\d+', '', text2)
    # remove punctuations and convert characters to lower case
    text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation]) 
    # substitute multiple whitespace with single whitespace
    # Also, removes leading and trailing whitespaces
    text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
    return text_no_doublespace


def extracttext(pdffile):
    pdfFileObj = open(pdffile, 'rb')
    # The pdfReader variable is a readable object that will be parsed.
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # Get the number of pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    # The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText()
    # This if statement exists to check if the above library returned words.
    # It's done because PyPDF2 cannot read scanned files
    if text != "":
        text = text
        # If the above returns as False, we run the OCR library textract to
        # convert scanned/image based PDF files into text.
    else:
        print('OCR!')
        text = textract.process(pdffile, method='tesseract',
                                language='eng')
        
    # The word_tokenize() function will break our text phrases into
    # individual words.
    text_clean = clean_text(str(text))
    # Create a list of words
    tokens = word_tokenize(text_clean)
    # Remove 1 & 2 letter words
    tokens2 = [x for x in tokens if len(x) > 2]
    # We'll create a new list that contains punctuation we wish to clean.
    # punctuations = ['(', ')', ';', ':', '[', ']', ',', '\\n']
    # We initialize the stopwords variable, which is a list of words like
    # "The," "I," "and," etc. that don't hold much value as keywords.
    stop_words = stopwords.words('english')
    # We create a list comprehension that only returns a list of words
    # that are NOT IN stop_words and NOT IN punctuations.
    keywords = [word for word in tokens2 if not word in stop_words] # and not word in punctuations]
    # Store keywords for paper
    return keywords


data = pd.DataFrame([], columns=['id_file', 'keywords'])
files = pd.read_pickle('/mnt/c/DATAscratch/SIPG/ICESfiles.pk')

# Process files
for i, _file in enumerate(files['id_file']):
    pdffile = '/mnt/c/DATAscratch/SIPG/pdf/'+str(int(_file))+'.pdf'
    # Test if file exists
    if os.path.exists(pdffile) & (not os.path.exists(pdffile+'.pk')):
        print(pdffile)
        try:
            keywords = extracttext(pdffile)
            _data = {'id_file': int(_file), 'keywords': keywords}
            __data = pd.DataFrame.from_dict(_data)
            __data.to_pickle(pdffile+'.pk')
            #data = pd.concat([data, __data], ignore_index = True)
        except:
            print('Failed reading')


