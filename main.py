from src.data_loader import ImageCaptioningDataset
from src.model import Transformer_model
from src.dataset_downloader import CreateImageDataset
import sys
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor
from PIL import Image
import requests

if __name__ == "__main__": 

    if len(sys.argv) < 2:
        print("Usage: python main.py test_image_url")
        sys.exit(1)

    test_image_url = sys.argv[1]

    repo_url = "https://github.com/marcusklasson/GroceryStoreDataset/archive/refs/heads/master.zip"
    destination_folder = "./data"
    images_folder = "./grocery_store_images"

    # creating the training image dataset 
    create_image_dataset = CreateImageDataset(repo_url, destination_folder, images_folder)
    create_image_dataset.downloader()
    captions = create_image_dataset.create_dictionary()
    dataset = create_image_dataset.create_dataset(captions)
    print(dataset)

    # load the dataset using Pytorch Dataset class
    processor = AutoProcessor.from_pretrained("microsoft/git-base")
    train_dataset = ImageCaptioningDataset(dataset, processor)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=5) # adjust batch size according to your GPU memory

    # define the model and train it 
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base")
    Transformer = Transformer_model(model)
    model = Transformer.model_train(2, train_dataloader) # first argument is the number of epochs

    # Inferencing the model
    image = Image.open(requests.get(test_image_url, stream=True).raw)
    caption = Transformer_model.model_inference(image, processor, model)
    print(f"Caption: {caption}")









   
