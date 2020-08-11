from bs4 import BeautifulSoup as bs
from splinter import Browser
from config import exe_path
import pandas as pd
import requests

def scrape ():
    mars_scrape = {}

    executable_path = {'executable_path':exe_path}
    browser = Browser('chrome', **executable_path)

    # Nasa Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('div', class_="list_text")
    news_title = results.find('a').text.strip('\n')
    news_p = soup.find('div', class_="article_teaser_body").text

    mars_scrape['news_title'] = news_title
    mars_scrape['news_p'] = news_p

    
    # JPL Mars Space Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    browser.click_link_by_id("full_image")
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('a', class_="button", target="_top")
    partial_href = results['href']
    browser.click_link_by_partial_href(partial_href)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('figure', class_="lede")
    link = results.find('a')
    partial_href = link['href']
    url_head = url.split('?')
    url_head2 = url_head[0].rsplit('/', maxsplit=2)
    featured_image_url = url_head2[0] + partial_href

    mars_scrape['featured_image_url'] = featured_image_url

    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-1mi0q7o")
    spans = results.find_all('span')
    mars_weather = spans[4].text

    mars_scrape['mars_weather'] = mars_weather

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Name', 'Value']
    df.set_index('Name', inplace=True)
    html_string = df.to_html()
    html_string = html_string.replace('\n', '')

    mars_scrape['html_string'] = html_string

    # Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_="item")
    partial_href = results[0].find('a')['href']

    # need more code here to finish this section

    mars_scrape['hemisphere_image_urls'] = hemisphere_image_urls

    return(mars_scrape)
