# Image captioning project
The goal of this project is to fine-tune an image captioning model and then use it for inference. 

We focused the specific scope to grocery store products images: they were retrieved from the following repository: https://github.com/marcusklasson/GroceryStoreDataset/tree/master, and transformed into a dataset made of image-caption couples for the fine-tuning.

# Project Structure
```
project-root/
│
├── src/
│ ├── data__loader.py
│ └── dataset_downloader.py
│ └── model.py
| └── web_scraping.py (Initially we were supposed to retrieve the images by scraping)
|
│── build.sh
├── model_pipeline.ipynb (Jupyter notebook for running the project on Colab)
├── main.py
├── requirements.txt
└── README.md
```
## Installation 
```
chmod +x build.sh 
./build.sh test_image_url
```
## Inference Test
![Alt text](https://imagedelivery.net/olI9wp0b6luWFB9nPfnqjQ/res/abillionveg/image/upload/tdhgiowbjngikopye2j2/1648938250.jpg/w=480)

"a carton of milk" 