from bs4 import BeautifulSoup as bs
from splinter import Browser
from config import exe_path
import pandas as pd
import requests
import time

def scrape ():
    # Initialize the dictionary that will be returned
    mars_scrape = {}

    # Inititate Splinter browser
    executable_path = {'executable_path':exe_path}
    browser = Browser('chrome', **executable_path)

    # -----------------------#
    #     Nasa Mars News     #
    # -----------------------#
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # pause to give the page time to load
    time.sleep(2)

    # Pull html code from web page and allow BeautifulSoup to parser through the code
    html = browser.html
    soup = bs(html, 'html.parser')

    # pause to give the parser time to parse
    time.sleep(3)

    # Search for the first article on the page and pull the title and synopsis paragraph
    results = soup.find('div', class_="list_text")
    news_title = results.find('a').text.strip('\n')
    news_p = soup.find('div', class_="article_teaser_body").text

    # Add the article title and paragraph to the dictionary that is to be returned
    mars_scrape['news_title'] = news_title
    mars_scrape['news_p'] = news_p

    # -----------------------#
    #  JPL Mars Space Image  #
    # -----------------------#
    # Load next url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Pull html code from web page and allow BeautifulSoup to parser through the code    
    html = browser.html
    soup = bs(html, 'html.parser')

    # Click on the link to the featured image
    browser.click_link_by_id("full_image")

    # pause to give the page time to load
    time.sleep(2)

    # Pull html code from web page and allow BeautifulSoup to parser through the code
    html = browser.html
    soup = bs(html, 'html.parser')

    # pause to give the parser time to parse
    time.sleep(3)

    # Find the link to the description page for the featured image & click the link
    results = soup.find('a', class_="button", target="_top")
    partial_href = results['href']
    browser.click_link_by_partial_href(partial_href)
    
    # Pull html code from web page and allow BeautifulSoup to parser through the code
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the featured image link and save the link
    results = soup.find('figure', class_="lede")
    link = results.find('a')
    partial_href = link['href']

    # break apart the url used to get to this page to extract the first part of it
    url_head = url.split('?')
    url_head2 = url_head[0].rsplit('/', maxsplit=2)

    # combine the first part of the base url and the link to the feature image together
    featured_image_url = url_head2[0] + partial_href

    # Add the scraped information from the url to the dictionary that is to be returned
    mars_scrape['featured_image_url'] = featured_image_url

    # -----------------------#
    #      Mars Weather      #
    # -----------------------#
    # Load the next url
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # pause to give the page time to load
    time.sleep(2)

    # Pull html code from web page and allow BeautifulSoup to parser through the code
    html = browser.html
    soup = bs(html, 'html.parser')

    # pause to give the parser time to parse
    time.sleep(2)

    # Find the desired information
    results = soup.find('div', class_="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-1mi0q7o")
    spans = results.find_all('span')
    mars_weather = spans[4].text

    # Add the scraped information from the url to the dictionary that is to be returned
    mars_scrape['mars_weather'] = mars_weather

    # -----------------------#
    #       Mars Facts       #
    # -----------------------#
    # Load the next url
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # put the tables on the page into a list of Dataframes
    tables = pd.read_html(url)

    # Extract the desired DataFrame (there is only one on this page)
    df = tables[0]

    # Name the DataFrame columns
    df.columns = ['Name', 'Value']

    # Reset the index to be the Name columns
    df.set_index('Name', inplace=True)

    # Convert the Dataframe into an html table
    html_string = df.to_html()

    # Strip the \n characters out of the html table code
    html_string = html_string.replace('\n', '')
    html_string = html_string.replace(' style="text-align: right;"', '')

    # Add the scraped information from the url to the dictionary that is to be returned
    mars_scrape['html_string'] = html_string

    # -----------------------#
    #    Mars Hemispheres    #
    # -----------------------#
    # Load the next url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Initialize an empty list to hold the scraped information
    hemisphere_image_urls = []

    # Pull html code from web page and allow BeautifulSoup to parser through the code
    html = browser.html
    soup = bs(html, 'html.parser')

    # break apart the url used to get to this page to extract the first part of it
    base_url = url.split('/search/')
    base_url[0]

    # Find the information for the four hemispheres
    results = soup.find_all('div', class_="item")
    
    # loop through the four items in the results list
    for x in range(0,4):
        # Extract the name of the hemisphere and strip off the word Enhanced
        raw_title = results[x].find('h3').text
        title = raw_title.replace(" Enhanced", "")

        # Extract the second part of the url then join the two parts together
        partial_href = results[x].find('a')['href']
        full_href = base_url[0] + partial_href

        # Vist the url that was just created        
        browser.visit(full_href)

        # Pull html code from web page and allow BeautifulSoup to parser through the code
        html = browser.html
        soup = bs(html, 'html.parser')

        # Search the new results for the image url
        results2 = soup.find_all('div', class_="wide-image-wrapper")
        link = results2[0].find('img', class_="wide-image")
        href = link['src']
        full_url = base_url[0] + href

        # Add the name and image url to the list as a dictionary
        hemisphere_image_urls.append({"title":title, "img_url":full_url})

    # Add the scraped information from the url to the dictionary that is to be returned
    mars_scrape['hemisphere_image_urls'] = hemisphere_image_urls

    # close the browser
    browser.quit()

    # Return the dictionary of all the scraped information
    return(mars_scrape)
