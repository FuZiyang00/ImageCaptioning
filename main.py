from dataset_utils import ImageCaptioningDataset, TrainDataset
from model_utils import Model
from transformers import AutoProcessor

if __name__ == "__main__":
    # Define folder paths
    folder_path = "/ImageCaptioning/Vegetables"
    destination_folder = "/ImageCaptioning/images"
    
    # Create vegetable dictionary
    captions = ImageCaptioningDataset.create_vegetable_dictionary(folder_path, destination_folder)
    print("The model will be trained on ", len(captions), " items.")
    print(captions)

    # Load and prepare dataset
    dataset = ImageCaptioningDataset.handle_dataset(destination_folder, captions)
    
    processor = AutoProcessor.from_pretrained("microsoft/git-base")
    train_dataset = TrainDataset(dataset, processor)

    train_dataloader = ImageCaptioningDataset.train_dataload(train_dataset)

    # Define and train model
    model = Model.train_model(train_dataloader)

    # Generate caption for an image
    img_path = '/ImageCaptioning/inference_images/onion.png'
    generated_caption = Model.use_model(img_path, processor)
    print("Generated caption:", generated_caption)
