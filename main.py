from web_scraping import Web_scraper

if __name__ == "__main__": 

    url = 'https://www.carrefour.it/spesa-online/dolci-e-prima-colazione/'
    web_scraper = Web_scraper(url)

    links, title = web_scraper.get_images()

    web_scraper.download_images(links, title)