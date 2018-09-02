
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib3
import pandas as pd
from newspaper import Article
from aylienapiclient import textapi


urls = [
            'https://www.marketwatch.com/search?q=appl',
            'https://www.marketwatch.com/search?q=TSLA',
            'https://www.marketwatch.com/search?q=FB',
            'https://www.marketwatch.com/search?q=AMZN',
            'https://www.marketwatch.com/search?q=NFLX',
            'https://www.marketwatch.com/search?q=CSCO',
            'https://www.marketwatch.com/search?q=GOOGL',
            'https://www.marketwatch.com/search?q=BIDU',
            'https://www.marketwatch.com/search?q=BABA',
            'https://www.marketwatch.com/search?q=tcehy'
        ]
client = textapi.Client("2e2625eb", "cb454a03eddd0b059bdf522d156ee40e")


# In[2]:


def get_url_by_company(x):
    http = urllib3.PoolManager()
    response = http.request('GET', x)
    label_value = x.split('=')[1]
    soup = BeautifulSoup(response.data,'html.parser')
    result_link = []
    data = soup.findAll('div',attrs={'class':'searchresult'})
    for div in data:
        links = div.findAll('a')
        #print(links)
        for a in links:
            #print(a['href'])
            result_link.append(a['href'])
    result_link = list(map(lambda x: str.replace(x, "http:", "https:"), result_link))
    #print(result_link)
    df = pd.DataFrame({'page_urls':result_link,'label':label_value})
    #df_parent.append(df)
    #print(df)
    return df


# In[3]:


def get_article_data_by_url(x):
    #x = 'https://www.marketwatch.com/story/weekend-roundup-should-apple-buy-tesla-a-no-deal-brexit-marijuana-stocks-and-politics-2018-08-31'    
    toi_article = Article(x, language="en") # en for English

    #To download the article
    toi_article.download()

    #To parse the article
    toi_article.parse()
    
    #To perform natural language processing ie..nlp
    toi_article.nlp()

    sentiment = client.Sentiment({'url': x})
    hashtags = client.Hashtags({'url':x})
    hashtag_values = ','.join(map(str, hashtags['hashtags']))

    article_list = [[x,toi_article.title,toi_article.text,toi_article.summary,sentiment['polarity'],
                     sentiment['polarity_confidence'],hashtag_values]]
    #print(article_list)

    #article_list.columns = ['page_urls','title','text','summary','article_sentiment','sentiment_confidence',
    #                           'article_hastags']
    return article_list


# In[4]:


df_parent = pd.DataFrame()
for url in urls:
    print(url)
    #get_url_by_company(url)
    temp_df = get_url_by_company(url)
    #print(temp_df)
    df_parent = df_parent.append(temp_df)
    
#print(df_parent)


# In[ ]:


article_data_df = pd.DataFrame()
for index, row in df_parent.iterrows():
    #print(row["page_urls"])
    temp_list = get_article_data_by_url(row["page_urls"])
    article_data_df = article_data_df.append(temp_list) 
    
article_data_df.columns = ['page_urls','title','text','summary','article_sentiment','sentiment_confidence',
                           'article_hastags']
#article_data_df


# In[ ]:


#article_data_df


# In[ ]:


final_df = df_parent.merge(article_data_df, left_on='page_urls', right_on='page_urls', how='left')


# In[ ]:


final_df

