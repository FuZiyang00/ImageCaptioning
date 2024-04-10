from transformers import AutoProcessor
import torch
from PIL import Image
import numpy as np

def get_processor():
    processor = AutoProcessor.from_pretrained("microsoft/git-base")
    return processor

def generate_caption_for_image(model, img_path):
    # Load the image
    img = Image.open(img_path)

    # Preprocess the image
    
    inputs = processor(images=img, return_tensors="pt")
    pixel_values = inputs.pixel_values

    # Move model and inputs to the appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    pixel_values = pixel_values.to(device)

    # Generate caption
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return generated_caption
