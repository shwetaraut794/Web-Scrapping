#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries 

from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib
import pandas as pd


# In[49]:


#Connect to the website to pull data
def extract(page):
    URL = f'https://www.amazon.com/gp/new-releases/amazon-devices/ref=zg_bsnr_pg_2?ie=UTF8&pg={page}'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36", 'Accept-Language': 'en-US, en;q=0.5'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def transform(soup):
    info = soup.find_all('div', class_ = 'zg-grid-general-faceout')
    for items in info:
        title = items.find('div', class_ = ['_cDEzb_p13n-sc-css-line-clamp-3_g3dy1','_cDEzb_p13n-sc-css-line-clamp-4_2q2cc']).text.strip()
        price = items.find('span', class_ ='_cDEzb_p13n-sc-price_3mJ9Z')
        #print(price)
        try:
            stars = items.find('div', class_ ='a-row').find('span', class_ = 'a-icon-alt').text.strip()
        except:
            stars = 'Not Provided'
        try:
            numberofreviews = items.find('div', class_ ='a-row').find('span', class_ = 'a-size-small').text.strip()
        except:
            numberofreviews = 'Not Provided'
        links = items.find('a', class_ = 'a-link-normal').get('href')
        link =  'https://www.amazon.com/' + links
        #print(link)
    
        products = {
                'Product Name' : title,
                'Product Price' : price,
                'Stars' : stars,
                'Number of Reviws' : numberofreviews,
                'Link' : link
        }
        productlist.append(products)
        
productlist = []  
for i in range (1,3,1):
    #print(f'Getting Page, {i}')
    c = extract(i)
    transform(c)

    
#print(len(productlist))

df = pd.DataFrame(productlist)

print(df.head())

df.to_csv('Amazon products.csv')


# In[ ]:




