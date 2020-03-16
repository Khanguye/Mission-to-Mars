#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)
#####################################################
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#------
# Optional delay for loading the page waiting for 1 sec before finding
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1) # Return True or False so need to check before
#open broswer and read html
html = browser.html
#give html stream to BeautifulSoup to parse
news_soup = BeautifulSoup(html, 'html.parser')
#select element the match tag id or class query
slide_elem = news_soup.select_one('ul.item_list li.slide')
#Find a child and get inner text
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
print(news_title)
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
print(news_p)
##########################################################
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
#---
#Browse and click the full image button
full_image_elem = browser.find_by_id('full_image')
#fire a event mouse click
full_image_elem.click()
#Browse more info text but waiting for 1 sec page load
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
# tream html data 
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')
# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
print(img_url_rel)
# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
print(img_url)
#######################################################
#Panda scraping tables in the webpage
#Read HTML tables into a ``list`` of ``DataFrame`` objects
#Get the 1 st one
df = pd.read_html('http://space-facts.com/mars/')[0]
#Rename columns
df.columns=['description', 'value']
#Reset index
df.set_index('description', inplace=True)
print(df)
#Pandas also has a way to easily convert our DataFrame back into HTML-ready code
print(df.to_html())
########################################################
#turning off browser after this is done
browser.quit()






