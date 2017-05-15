# -*- coding: utf-8 -*-
"""
Created on Sun May 07 07:07:30 2017

@author: Hyun Do Im
"""

###Certification Program

#Since the website is written in Java Script, I will not use bs4, but selenium
#Importing Selenium and its functions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
import json
from textblob import TextBlob
import tweepy
from string import punctuation
import codecs
import re

#Dictionary to contain the actor/actress' information
celeb_info={}
celeb_name=[]
tweets_dict={}

 #Consumer key and secret from Twitter
ckey = "B6zKKY0pwDaGBbO0NUISDaY6P"
csecret = "7kCi5kh89yxjKkRKB05uQTbp4QAbMkMxpqymwnYYBWUptLedHx"

#Access token and access secret 
atoken = "862549276961808384-Y0oyynhYT3XTi05BrGa393AFS08RFpp"
asecret = "830xLJSpwFH2KkQhnT1Z0AzoDm6A01JQoW4jQOx8jPKDF"

#QAuth Authentication
auth = tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
#Wrapping twitter API
api = tweepy.API(auth)



"""C:\\Users\\Hyun Do Im\\Downloads\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe"""
def scraping():
    #Use PhantonJS.exe
    driver = webdriver.PhantomJS("C:\\Users\\Hyun Do Im\\Downloads\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    #Through PhantomJS get excess to "http://m.imdb.com/feature/bornondate"
    driver.get("http://m.imdb.com/feature/bornondate")
    element = Wait(driver,10)
    #Assign specific area of html that I want to engage
    posters=element.until(EC.presence_of_element_located((By.CSS_SELECTOR,"section.posters")))
    
    for a in posters.find_elements_by_css_selector('a.poster'):
        person = a.find_element_by_css_selector('div.detail').text
        title = a.find_element_by_css_selector('span.title').text
        img = a.find_element_by_tag_name('img').get_attribute('src').split('._V1.')[0]+'._V1_SX214_AL_.jpg'
        #distinguishing profession and best work of the celeb from imported data
        profession=person.split(",")[0]
        best_work=person.split(",")[1]
        #print the information that I obtained from the web
        print title,":", person, "\n",img
        #Storing data into my dictionary
        celeb_info[title] = title, img, profession, best_work
        #Saving names to name list
        celeb_name.append(title)
    driver.close()

def tweet_search():
    #tweets_dict[celeb_name[0]] = api.search(celeb_name[0],count = 100)
    
    for i in range(10):
        tweets1 = api.search(celeb_name[i],count = 100)    
        def analysis_():
            for items in tweets1:
                
                analysis = TextBlob(items.text)
                if analysis.sentiment.polarity>0:
                    return 'positive'
                elif analysis.sentiment.polarity<0:
                    return 'negative'
                else:
                    return 'neutral'
        tweets_dict[celeb_name[i]] = analysis_()

def Output():
    for i in range(10):
        print "The Name of Celebrity: "+celeb_name[i]+"\n"+ "Profession: "+celeb_info[celeb_name[i]][2]+ "\n"+ "Best Work: "+celeb_info[celeb_name[i]][3]+"\n"+"Celebrity Image: " + celeb_info[celeb_name[i]][1] + "\n" + "Sentiment: " + tweets_dict[celeb_name[i]]
    