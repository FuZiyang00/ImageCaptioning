from transformers import AutoProcessor
from transformers import AutoModelForCausalLM
from evaluate import load
import torch
from transformers import TrainingArguments, Trainer

class ImageCaptioningModel:
    def __init__(self, model_name):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model = self.model.to('cpu')
        self.wer = load("wer")

    def transforms(self, example_batch):
        images = [x for x in example_batch["image"]]
        captions = [x for x in example_batch["text"]]
        inputs = self.processor(images=images, text=captions, padding="max_length")
        inputs.update({"labels": inputs["input_ids"]})
        return inputs
    
    def compute_metrics(self, eval_pred):
        logits, labels = eval_pred
        predicted = logits.argmax(-1)
        decoded_labels = self.processor.batch_decode(labels, skip_special_tokens=True)
        decoded_predictions = self.processor.batch_decode(predicted, skip_special_tokens=True)
        wer_score = self.wer.compute(predictions=decoded_predictions, references=decoded_labels)
        return {"wer_score": wer_score}


    def training_args(self, model_name):
        name = model_name.split("/")[1]
        training_args = TrainingArguments(
                output_dir=f"{name}-carrefour",
                learning_rate=5e-5,
                num_train_epochs=50,
                fp16=True,
                per_device_train_batch_size=32,
                per_device_eval_batch_size=32,
                gradient_accumulation_steps=2,
                save_total_limit=3,
                evaluation_strategy="steps",
                eval_steps=50,
                save_strategy="steps",
                save_steps=50,
                logging_steps=50,
                remove_unused_columns=False,
                label_names=["labels"],
                load_best_model_at_end=True,
            )
        
        return training_args
    

    def train(self, train_ds, test_ds, training_args):
        
        trainer = Trainer(
                model=self.model,
                args= training_args,
                train_dataset=train_ds,
                eval_dataset=test_ds,
                compute_metrics=self.compute_metrics,)
        
        trainer.train()
        
