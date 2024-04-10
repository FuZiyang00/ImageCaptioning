from transformers import AutoModelForCausalLM
import torch
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Model():
    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/git-base")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def train_model(self, train_dataloader):

        optimizer = torch.optim.AdamW(self.model.parameters(), lr=5e-5)

        self.model.to(self.device)

        self.model.train()

        for epoch in range(50):
            print("Epoch:", epoch)
            for idx, batch in enumerate(train_dataloader):
                input_ids = batch.pop("input_ids").to(self.device)
                pixel_values = batch.pop("pixel_values").to(self.device)
                outputs = self.model(input_ids=input_ids,
                                pixel_values=pixel_values,
                                labels=input_ids)

                loss = outputs.loss

                print("Loss:", loss.item())

                loss.backward()

                optimizer.step()
                optimizer.zero_grad()

    def use_model(self, img_path, processor):

        img = mpimg.imread(img_path)

        plt.imshow(img)
        plt.axis('off')
        plt.show()

        inputs = processor(images=img, return_tensors="pt").to(self.device)
        pixel_values = inputs.pixel_values

        generated_ids = self.model.generate(pixel_values=pixel_values, max_length=50)
        generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_caption
