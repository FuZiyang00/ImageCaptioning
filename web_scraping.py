from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import requests
import os
import time
import re

class Web_scraper: 

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()  # Change this to your preferred WebDriver
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}

    
    def get_images(self):
        self.driver.get(self.url)
        # Auto-scroll to the bottom of the page to load more images
        
        #last_height = self.driver.execute_script("return document.body.scrollHeight")
        #while True:
        #    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #    time.sleep(2)  # Adjust the sleep time as needed
        #    new_height = self.driver.execute_script("return document.body.scrollHeight")
        #    if new_height == last_height:
        #        break
        #    last_height = new_height
        
        scroll_count = 0
        while scroll_count < 10:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_count += 1

        # Parse the HTML content after auto-scrolling
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Extract all img tags with class img
        images = bs.find_all('img', attrs={'class':'tile-image lazyload'})
        print(images[0])

        links = [listing['data-srcset'].split(' ')[0].strip() for listing in images]
        print(links[0])
        
        title = [listing['title'] for listing in images]

        return links, title
    
    def clean_title(self, title):
        # Remove invalid characters from title using regex
        cleaned_title = re.sub(r'[\\/*?:"<>|]', '', title)
        return cleaned_title

    def download_images(self, links, title):
        count = 0

        if not os.path.exists('images'):
            os.makedirs('images')
        
        print(f"Total links: {len(links)}, Total titles: {len(title)}")  # Debugging line
        
        for i in tqdm(range(len(links))):
            if i >= len(title):
                print(f"Index {i} out of range for titles list.")  # Debugging line
                break

            cleaned_title = self.clean_title(title[i])  # Corrected variable name
            with open(f'images/{cleaned_title}.jpg', 'wb') as f:
                f.write(requests.get(links[i]).content)
                count += 1
                time.sleep(1)
            if count == 100:
                break

        print(f'{count} images downloaded successfully')

        print(f'{count} images downloaded successfully')

    def close_driver(self):
        self.driver.quit()