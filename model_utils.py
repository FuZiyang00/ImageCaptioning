from transformers import AutoModelForCausalLM
import torch
from torch.utils.data import DataLoader

def get_pretrained_model():

    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base")
    
    return model

def train_model(model, train_dataloader, num_epochs=50):

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    model.train()

    for epoch in range(num_epochs):
        print("Epoch:", epoch)
        for idx, batch in enumerate(train_dataloader):
            input_ids = batch.pop("input_ids").to(device)
            pixel_values = batch.pop("pixel_values").to(device)
            outputs = model(input_ids=input_ids,
                            pixel_values=pixel_values,
                            labels=input_ids)

            loss = outputs.loss

            print("Loss:", loss.item())

            loss.backward()

            optimizer.step()
            optimizer.zero_grad()
