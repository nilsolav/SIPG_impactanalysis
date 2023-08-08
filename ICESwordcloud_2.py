def plotwordcloud(text, filename):
    text = str(text).replace("', '", " ")
    text = str(text).replace("[[',", "")
    text = str(text).replace("']]", "")

    wordcloud = WordCloud(width = 800, height = 800, 
                          background_color ='white', 
                          stopwords = stop_words, 
                          min_font_size = 10).generate_from_text(text)
    
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.savefig(filename)
    plt.close()

plotwordcloud(dat[0:1],'/mnt/c/DATAscratch/SIPG/ICESwordcloud.png')
