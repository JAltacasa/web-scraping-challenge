from bs4 import BeautifulSoup 
import pymongo
from splinter import Browser
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path': 'C:\webdrivers\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    executable_path = {'executable_path': 'C:\webdrivers\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #title retrieval
    title_news = soup.find("div", class_="content_title").text
    
    #headline retrieval
    firstline_news = soup.find("div", class_="article_teaser_body").text

    #retrieving main image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    # retrieving weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather = soup.find('p', class_="tweet-text")

    # retrieving facts
    url = "http://space-facts.com/mars/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    facts_df = pd.read_html('https://space-facts.com/mars/')[0]
    fact_df.columns = ["Description", "Value"]
    facts_df = facts_df.to_html(index = True, header =True)

    # retrieving hemisphere images
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    root_url = "https://astrogeology.usgs.gov"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    xpath = "//div[@class='description']//a[@class='itemLink product-item']/h3"
    results = browser.find_by_xpath(xpath)
    results[0].html
    hemisphere_image_urls = []

    for i in range(4):

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = browser.find_by_xpath(xpath)
        header = results[i].html
        details_link = results[i]
        details_link.click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Saving the image url
        hemisphere_image_urls.append({"title": header, "image_url": soup.find("div", class_="downloads").a["href"]})
    
    # Going back to the original page
    browser.back()

    

    used_data = {
        "title_news": news_title,
        "firstline_news": firstline_news,
        "featured_image_url": featured_image_url,
        "weather": weather,
        "facts_df":facts_df,
        "hemisphere_image_urls":hemisphere_image_urls
        }

    return used_data