import os
import shutil
import json
from datasets import load_dataset
from torch.utils.data import Dataset

def create_vegetable_dictionary(folder_path, destination_folder):
    captions = []
    # Iterate through each item in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Check if it's a directory
        if os.path.isdir(item_path):
            # Recursively call the function for subdirectories
            captions.extend(create_vegetable_dictionary(item_path, destination_folder))
        else:
            # Check if it's a description file
            if item.endswith('_Description.txt'):
                # Extract vegetable type from the file name
                vegetable_type = os.path.splitext(item)[0].replace('_Description', '')

                # Check if corresponding image file exists
                image_file = os.path.join(folder_path, f"{vegetable_type}_Iconic.jpg")
                if os.path.exists(image_file):
                    # Create destination folder if it doesn't exist
                    os.makedirs(destination_folder, exist_ok=True)

                    # Check if the image file doesn't exist in the destination folder
                    destination_image_file = os.path.join(destination_folder, os.path.basename(image_file))
                    if not os.path.exists(destination_image_file):
                        # Move image to the destination folder
                        shutil.copy(image_file, destination_folder)

                    with open(item_path, 'r') as f:
                        description_text = f.read()

                    captions.append({
                        "file_name": os.path.basename(image_file),
                        "text": description_text
                    })

    return captions

def handle_dataset(root, captions):
    with open(root + "/metadata.jsonl", 'w') as f:
        for item in captions:
            f.write(json.dumps(item) + "\n")

    dataset = load_dataset("imagefolder", data_dir=root, split="train")
    return dataset

class ImageCaptioningDataset(Dataset):
    def __init__(self, dataset, processor):
        self.dataset = dataset
        self.processor = processor

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]

        encoding = self.processor(images=item["image"], text=item["text"], padding="max_length", return_tensors="pt")

        # remove batch dimension
        encoding = {k:v.squeeze() for k,v in encoding.items()}

        return encoding
