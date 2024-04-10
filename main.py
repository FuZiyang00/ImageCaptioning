from dataset_utils import create_vegetable_dictionary, handle_dataset, ImageCaptioningDataset
from model_utils import get_pretrained_model, train_model
from inference_utils import get_processor, generate_caption_for_image

def main():
    # Define folder paths
    folder_path = "/ImageCaptioning/Vegetables"
    destination_folder = "/ImageCaptioning/images"
    
    # Create vegetable dictionary
    captions = create_vegetable_dictionary(folder_path, destination_folder)
    print("The model will be trained on ", len(captions), " items.")
    print(captions)

    # Load dataset
    dataset = handle_dataset(destination_folder, captions)
    
    # Define and train model
    model = get_pretrained_model()

    processor = get_processor()
    train_dataset = ImageCaptioningDataset(dataset, processor)
    
    train_model(model, dataset)

    # Generate caption for an image
    img_path = '/content/drive/MyDrive/onion.jpg'
    generated_caption = generate_caption_for_image(model, img_path)
    print("Generated caption:", generated_caption)

if __name__ == "__main__":
    main()
