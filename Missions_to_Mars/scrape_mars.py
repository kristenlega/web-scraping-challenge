
# dependencies
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    final_dict={}
    news_title = 0

    # NASA MARS ARTICLE
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url, headers={'Cache-Control': 'no-cache'})
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # Parse the page for the first "content_title" element
    news_title = soup.find('div', class_="content_title").text.strip()
    # Parse the page for the first "rollover_description_inner" element
    news_p = soup.find('div', class_="rollover_description_inner").text

    # JPL MARS SPACE IMAGES
    imageurl="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(imageurl)
    html = browser.html
    imgsoup = BeautifulSoup(html, 'html.parser')
    # find URL suffix div
    short_url = imgsoup.find('img', class_="headerimage fade-in")
    # clean up the URL
    short_url_clean = short_url['src']
    # add the URL suffix to the base URL
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{short_url_clean}'

    # MARS FACTS
    factsurl="https://space-facts.com/mars/"
    # read the HTML into a db with pandas
    factstable = pd.read_html(factsurl)
    # set the column names
    factstable[0].columns = ['Description','Mars']
    # set the index
    factstable[0].set_index("Description",inplace=True)
    # set back to html
    factstable_html = factstable[0].to_html()
    # remove the line break characters
    factstable_html.replace('\n','')

    # MARS HEMISPHERES
    hemi_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    html = browser.html
    hemisoup = BeautifulSoup(html, 'html.parser')
    # find the collapsible results divs
    hemi_results = hemisoup.find("div", class_="collapsible results")
    # from those, pull out the items
    hemi_items = hemi_results.find_all("div", class_="item")

    hemisphere_image_urls = []

    # loop over results to get titles and urls
    for item in hemi_items:
        # scrape the image title
        description = item.find('div', class_='description')
        title = description.find('h3').text
        
        # scrape the image url
        hemi_page_url_short = item.a['href']
        
        # visit the new page
        browser.visit(f'https://astrogeology.usgs.gov{hemi_page_url_short}')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # find the downloads div
        downloads = soup.find("div", class_="downloads")
        # extract the image url
        img_url = downloads.find('li').a['href']
        
        # Create Dictionary Element
        hemi_dict = {
            'title': title,
            'img_url': img_url,
        }

        # Append to list
        hemisphere_image_urls.append(hemi_dict) 

    # Create the final dictionary
    final_dict={
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url":featured_image_url,
    "factstable_html":factstable_html,
    "hemisphere_images":hemisphere_image_urls}

    # Quit the browser
    browser.quit()

    return final_dict
