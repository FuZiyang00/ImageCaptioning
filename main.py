from web_scraping import Web_scraper

if __name__ == "__main__": 

    url = 'https://www.carrefour.it/spesa-online/dolci-e-prima-colazione/'

    browser = "Chrome"

    web_scraper = Web_scraper(url, browser)

    links, title = web_scraper.get_images()

    web_scraper.download_images(links, title)
    
    web_scraper.close_driver()