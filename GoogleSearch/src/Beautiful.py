
# coding: utf-8

# In[1]:

import urllib.request
import pandas as pd


# In[2]:

Sheet = pd.read_excel('../data/Data.xlsx', sheetname='Rohan')
Sheet['Ad value'] = ""
Sheet.columns


# ## IP Address Bouncer

# In[3]:

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
        'tutorial.randomproxy.RandomProxy': 100,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'tutorial.spiders.rotate_useragent.RotateUserAgentMiddleware' :400,
    }


# In[4]:

#the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
#for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php

user_agent_list = [    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
   ]



# In[5]:

import random

def process_request():
    ua = random.choice(user_agent_list)
    return ua


# ##  Ad Result

# In[6]:

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import bs4 as bs
import urllib
import pandas as pd
import re
import datetime

SearchTerm = ""

def get_google_search_results(keyword):
    address = "http://www.google.com/search?q=%s&num=100&hl=en&start=0" % (urllib.parse.quote_plus(keyword))
    user = process_request()
    request = urllib.request.Request(address, None, {'User-Agent':user})#'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
    urlfile = urllib.request.urlopen(request)
    page = urlfile.read()
    print(address)
    soup = bs.BeautifulSoup(page,'lxml')
    print(soup.title.string)
    SearchTerm = keyword
    return soup,address

def add_sheet(link):
    print("hi")

def scrape_ads(soup, phraseID, SearchTerm, address):
    """Scrape the text as HTML, find and parse out all the ads and store them in a database
    """    

    print("SearchTerm", SearchTerm)
    #get the ads on the right hand side of the page
    prices = soup.findAll('div', attrs={'class':'mnr-c pla-unit'})
    Mainads = soup.findAll('li', attrs={'class':'ads-ad'})
    Bottom = soup.findAll('div', attrs={'id':'bottomads'})
    position = 0
    
    result_block = soup.findAll('div', attrs={'class':'_Dw'})
    print("hello")
    for ad in result_block:
        site = ad.find('a',attrs={'class':'plantl'})['href']
        line1 = ad.find('span', attrs={'class': 'rhsl4'}).text
        Price = ad.find('span', attrs={'class': '_kh'}).text
        print(Price)
        position += 1
        arow2 = [datetime.datetime.now(), SearchTerm, address, site, 'NA',position, 'RHS', 'NA', '1','Sponsored Ad', 'NA',line1]
        Sheet.loc[len(Sheet)] = arow2

        
    position = 0
    #Main Ads    
    for ad in Mainads:
        position += 1
        #display url
        parts = ad.find('cite').findAll(text=True)
        site = ''.join([word.strip() for word in parts]).strip()
        ad.find('cite').replaceWith("")
        print(site)
 
        #the header line
        parts = ad.find('a').findAll(text=True)
        title = ' '.join([word.strip() for word in parts]).strip()
 
        #the destination URL
        href = ad.find('a')['href']
        start = href.find('&q=')
        if start != -1 :
            dest = href[start+3:]
        else :
            dest = None
            print ('error', href)
 
        ad.find('a').replaceWith("")
    
        #body of ad
        brs = ad.findAll('br')
        for br in brs:
            br.replaceWith("%BR%")
        parts = ad.findAll(text=True)
        body = ' '.join([word.strip() for word in parts]).strip()
        line1 = body.split('%BR%')[0].strip()
        #line2 = body.split('%BR%')[1].strip()
        #['Datetime', 'Search term', 'Google URL ', 'Ad URL Website', 'Vendor','Position Num', 'Position', 'Result is consistent', 'Page number','Type of result', 'Comments', 'Ad value']
        arow2 = [datetime.datetime.now(), SearchTerm, address, site, 'NA',position, 'Main Ad', 'NA', '1','Sponsored Ad', 'NA',line1]
        Sheet.loc[len(Sheet)] = arow2



def get_all_keywords():
    #Read the file
    df = pd.read_excel('../data/productsSample.xlsx', sheetname='Table1')
    ## Get the Search String
    queryString = df['model']+" "+df['brand'] ## if model number not present  -> product name 
    queryString = queryString.to_frame()
    queryString = queryString.rename(columns= {0: 'keywordPhrase'})
    queryString.insert(0, 'phraseID', range(1, 1 + len(queryString)))
    return queryString
        
def do_all_keywords():
    queryString = get_all_keywords()
    resultnew = queryString.head(n=10)
    for index, row in resultnew.iterrows():
        print (row['phraseID'], row['keywordPhrase'])
        soup, address = get_google_search_results(row['keywordPhrase'])
        print(address)
        scrape_ads(soup, row['phraseID'],row['keywordPhrase'],address)

    

if __name__ == '__main__' :
    do_all_keywords()        


# In[7]:

Sheet.to_csv('../data/Ads.csv')
#Sheet = Sheet.iloc[0:0]


# ## Organic Results
# 

# In[11]:

import requests
from bs4 import BeautifulSoup
import time

user = process_request()

USER_AGENT = {'User-Agent':user}


def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text, google_url


def parse_results(html, keyword, google_url):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            #print(link)
            title = title.get_text()
            description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description})
                rank += 1
                #['Datetime', 'Search term', 'Google URL ', 'Ad URL Website', 'Vendor','Position Num', 'Position', 'Result is consistent', 'Page number','Type of result', 'Comments', 'Ad value']
                arow2 = [datetime.datetime.now(), keyword, google_url, link, 'NA',rank, 'organic search', 'NA', '1','organic search', 'NA',title]
                Sheet.loc[len(Sheet)] = arow2
    return found_results


def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html, google_url = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword, google_url)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")
        
def get_all_keywords():
    #Read the file
    df = pd.read_excel('../data/productsSample.xlsx', sheetname='Table1')
    ## Get the Search String
    queryString = df['model']+" "+df['brand'] ## if model number not present  -> product name 
    return queryString

if __name__ == '__main__':
    keywords = get_all_keywords()#['iphone']
    data = []
    for keyword in keywords:
        try:
            results = scrape_google(keyword, 20, "en")
            for result in results:
                data.append(result)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
    #print(data)


# In[13]:

Sheet


# In[12]:

Sheet.to_csv('../data/Sheet.csv')


# In[ ]:




# In[ ]:



