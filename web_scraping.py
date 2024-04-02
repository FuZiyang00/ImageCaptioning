from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from tqdm import tqdm
import requests
import os
import time 

class Web_scraper: 

    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}
        
        self.req = Request(url, headers=self.headers)

    def get_images(self):
        response = urlopen(self.req)
        bs = BeautifulSoup(response.read(), 'html.parser')

        #  extract all img tags with class img
        images = bs.find_all('img', attrs={'class':'tile-image lazyload'})
        print(images[0]) # debugging purposes

        links = [listing['data-srcset'].split(' ')[0].strip() for listing in images]
        print(links[0]) # debugging purposes
        
        title = [listing['title'] for listing in images]

        return links, title
    
    def download_images(self, links, title):
        """
        create a folder to store the images
        """
        count = 0

        if not os.path.exists('images'):
            os.makedirs('images')
        
        for i in tqdm(range(len(links))):
            with open(f'images/{title[i]}.jpg', 'wb') as f:
                f.write(requests.get(links[i]).content)
                count += 1
                time.sleep(1)
            if count == 100:
                break

        print(f'{count} images downloaded successfully')
