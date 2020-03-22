#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path)
    
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    #turning off browser after this is done
    browser.quit()

    return data

#####################################################
def mars_news(browser):
    # Visit the mars nasa news site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    #------
    # Optional delay for loading the page waiting for 1 sec before finding
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1) # Return True or False so need to check before
    #open broswer and read html
    html = browser.html
    #give html stream to BeautifulSoup to parse
    news_soup = BeautifulSoup(html, "html.parser")
    try:
        #select element the match tag id or class query
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        #Find a child and get inner text
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_="content_title").get_text()
        #print(news_title)
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
   
    #print(news_p)
    return news_title, news_p
##########################################################
def featured_image(browser):
    # Visit URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    #---
    #Browse and click the full image button
    full_image_elem = browser.find_by_id("full_image")
    #fire a event mouse click
    full_image_elem.click()
    #Browse more info text but waiting for 1 sec page load
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()

    # Parse the resulting html with soup
    # tream html data 
    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one("figure.lede a img").get("src")
        #print(img_url_rel)
        # Use the base URL to create an absolute URL
        img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
    except AttributeError:
        return None

    #print(img_url)
    return img_url
#######################################################
def mars_facts():
    try:
        #Panda scraping tables in the webpage
        #Read HTML tables into a ``list`` of ``DataFrame`` objects
        #Get the 1 st one
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    #Rename columns
    df.columns=["description", "value"]
    #Reset index
    df.set_index("description", inplace=True)
    #print(df)
    #Pandas also has a way to easily convert our DataFrame back into HTML-ready code
    #print(df.to_html())

    return df.to_html() 
########################################################
################# CHALLENGE CODES ######################
########################################################
# Domain URL is used to scrape Mars surface
__DOMAIN_URL = 'https://astrogeology.usgs.gov'
########################################################
# scrape the Mars surface main function
def scrape_mars_surfaces():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path)

    # Scrapping mars surface data
    title_href_list = find_title_href(browser)
    data = find_highdef_image(browser, title_href_list)
    
    #turning off browser after this is done
    browser.quit()

    return data
#########################################################
# Find the title and follow link of each Mars surfaces
def find_title_href(browser):
    #Visit the main page
    url = f'{__DOMAIN_URL}/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #Scrape title and follow url (href)
    #Four sides of Mars
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div',class_='item')
    #Declare a list to hold dictionary item
    dicList = []
    for item in items:
        try:
            dicItem  = {}
            #get the title of Mars surface
            dicItem["title"] = item.find('h3').text
            #get the follow link url of Mars surface
            dicItem["href"] =  item.find('a')["href"]
            #add into the list
            dicList.append(dicItem)
        except AttributeError:
            continue
    return dicList
########################################################   
# find the high def images url from each follow href of each Mars Surface
def find_highdef_image(browser, title_href_list):
    #declare and assign dictionary list
    dicList = title_href_list
    #loop each dictionary item
    for dicItem in dicList:
        #Visit each Mars suface URL
        browser.visit(f'{__DOMAIN_URL}{dicItem["href"]}')
        #Use BeautifulSoup to parse html
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        try:
            sample =  soup.find('div',class_='downloads').find_all('a')[0]["href"]
            orginal = soup.find('div',class_='downloads').find_all('a')[1]["href"]
        except AttributeError:
            sample = ""
            orginal = ""
        #Add img_url 
        dicItem['img_url_jpg'] = sample   
        dicItem['img_url'] = orginal
        #remove href
        dicItem.pop('href')
    return dicList


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())






