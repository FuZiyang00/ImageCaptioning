from web_scraping import Web_scraper
from datasets import load_dataset 
from model import ImageCaptioningModel
import torch

if __name__ == "__main__": 

    # url = 'https://www.carrefour.it/spesa-online/dolci-e-prima-colazione/'

    # browser = "Firefox"
    # web_scraper = Web_scraper(url, browser)
    # links, title = web_scraper.get_images(20)
    # web_scraper.download_images(links, title)
    # web_scraper.driver.quit()

    path = 'images'
    # web_scraper.get_metadata(path)
    dataset = load_dataset("imagefolder", data_dir=path, split="train")
    print(dataset)
    dataset = dataset[:50]

    ds = dataset.train_test_split(test_size=0.1)
    train_ds = ds["train"]
    test_ds = ds["test"]

    model = ImageCaptioningModel("microsoft/git-base")
    train_ds.set_transform(model.transforms)
    test_ds.set_transform(model.transforms)
    training_args = model.training_args("microsoft/git-base")
    model.train(train_ds, test_ds, training_args)

