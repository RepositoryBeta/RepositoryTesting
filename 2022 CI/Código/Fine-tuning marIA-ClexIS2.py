import pandas as pd
import numpy as np
import unicodedata
import re
import os
import csv
import sklearn.metrics as metrics
from transformers import RobertaTokenizer, RobertaForMaskedLM
from torch.utils.data import Dataset, DataLoader
import torch
from transformers import RobertaForSequenceClassification, RobertaConfig
from transformers import Trainer, TrainingArguments
from transformers import EvalPrediction
from sklearn import metrics, feature_selection
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer


data_raw = pd.read_excel('C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/corpus/Español/CLexIS2_single_train.xlsx')

data_raw = data_raw[['sentence', 'token', 'complexity']]

data_raw['sentence'] = data_raw['sentence'].astype(str)
data_raw['token'] = data_raw['token'].astype(str)

data = pd.DataFrame(columns=['text', 'complexity'])
count = 0
for i in range(0, data_raw.shape[0]):
  data.loc[count] = [data_raw['sentence'][count].lower() + ' [SEP] ' + data_raw['token'][count].lower(), \
                    data_raw['complexity'][count]]
  count += 1

data

tokenizer = RobertaTokenizer.from_pretrained('C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA')

def vectorize_text(s, max_length):

    # Unicode normalization
    #s = s.strip().lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    # Remove undesired characters
    #s = re.sub(r'([.¿?()/'",;:$€])', r' /1 ', s)
    #s = re.sub(r"[^a-zA-Záéíóú.,!?;:()$€]+", r" ", s)

    # Text to tensor
    input_ids = tokenizer.encode(
      s,
      add_special_tokens=True,
      max_length=max_length,
      padding='longest', 
      truncation=True,
      return_tensors='np'
    )
    return input_ids[0]

data['text_vec'] = data.apply(lambda r: vectorize_text(r['text'], 512), axis=1)

data = data.sample(frac=1)
train_portion = 0.8
split_point = int(train_portion*len(data))
train_data, test_data =  data[:split_point], data[split_point:] 
print(len(train_data), 'train, ', len(test_data), 'test')



class MyDataset(Dataset):
    def __init__(self, dataframe):
        self.len = len(dataframe)
        self.data = dataframe
        
    def __getitem__(self, index):
        input_ids = torch.tensor(self.data.text_vec.iloc[index]).cpu()
        attention_mask = torch.ones([input_ids.size(0)]).cpu()
        targets = self.data.complexity.iloc[index]
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': targets
         }
            
    def __len__(self):
        return self.len

train_set, test_set = MyDataset(train_data), MyDataset(test_data)


config = RobertaConfig.from_pretrained('C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA')
config.problem_type='regression'
config.num_labels=1
model = RobertaForSequenceClassification.from_pretrained('C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA',config=config)

def collate_batch(batch):
    """ Optimize memory by setting all vectors in batch to a length equal to max
        length found
    """
    
    def pad_sequence(in_tensor, max_size):
        """ Fill tensor with zeros up to max_size
        """
        out_tensor = np.zeros(max_size)
        out_tensor[:in_tensor.size(0)] = in_tensor.numpy()
        return out_tensor
    
    batch_inputs = []
    batch_attention_masks = []
    batch_targets = []

    max_size = max([ex['input_ids'].size(0) for ex in batch])
    for item in batch:
        batch_inputs.append(pad_sequence(item['input_ids'], max_size))
        batch_attention_masks.append(pad_sequence(item['attention_mask'], max_size))
        batch_targets.append(float(item['labels']))
    return {
        "input_ids": torch.tensor(batch_inputs, dtype=torch.long),
        "attention_mask": torch.tensor(batch_attention_masks, dtype=torch.long),
        "labels": torch.tensor(batch_targets, dtype=torch.float)
    }

class MyTrainer(Trainer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def get_train_dataloader(self):
    return DataLoader(
        self.train_dataset,
        collate_fn=collate_batch
    )

  def get_eval_dataloader(self, eval_dataset):
    return DataLoader(
  
        self.eval_dataset,
        collate_fn=collate_batch
    )

## Para calcular nuestras propias métricas
def compute_metrics(p: EvalPrediction):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    preds = np.squeeze(preds)
    return {"MSE": ((preds - p.label_ids) ** 2).mean().item(),
            'R2': metrics.r2_score(p.label_ids, preds),
            'RMSE': metrics.mean_squared_error(p.label_ids, preds),
            'MAE': metrics.mean_absolute_error(p.label_ids, preds)}
            #'Poisson': metrics.mean_poisson_deviance(p.label_ids, preds)}
            #'Pearson': feature_selection.r_regression(p.label_ids, preds)}

training_args = TrainingArguments(
    output_dir='output',
    evaluation_strategy='steps',
    eval_steps=1000,
    num_train_epochs=2,
    remove_unused_columns=False,
    per_device_train_batch_size=256,
    per_device_eval_batch_size=256,
)

trainer = MyTrainer(
    model=model,
    args=training_args,
    train_dataset=train_set,
    eval_dataset=test_set,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.save_model("C:/Users/TIA/Desktop")