import math
from transformers import RobertaConfig
from transformers import RobertaForMaskedLM
from transformers import RobertaTokenizerFast
from datasets import load_dataset
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import torch
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

TRAIN_BATCH_SIZE = 16    # input batch size for training (default: 64)
VALID_BATCH_SIZE = 8    # input batch size for testing (default: 1000)
TRAIN_EPOCHS = 15        # number of epochs to train (default: 10)
LEARNING_RATE = 1e-4    # learning rate (default: 0.001)
WEIGHT_DECAY = 0.01
SEED = 42               # random seed (default: 42)
MAX_LEN = 128
SUMMARY_LEN = 7
tokenizer_folder = 'C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/token'
train_df=pd.read_excel('C:/Users/TIA/Desktop/CLexIS2_single_train.xlsx', header=0)
train_df.dropna(inplace=True)
test_df=pd.read_excel('C:/Users/TIA/Desktop/lcp_single_test.xlsx', header=0)
test_df.dropna(inplace=True)


#datasets = load_dataset("Cris1907/marIA-UG", data_files={"train": "train_ug.txt", "test": "train_ug2.txt"})
config = RobertaConfig(
    vocab_size=8192,
    max_position_embeddings=514,
    num_attention_heads=12,
    num_hidden_layers=6,
    type_vocab_size=1,
)

model = RobertaForMaskedLM(config=config)
print('Num parameters: ',model.num_parameters())

# Create the tokenizer from a trained one
tokenizer = RobertaTokenizerFast.from_pretrained(tokenizer_folder, max_len=MAX_LEN)

class CustomDataset(Dataset):
    def __init__(self, df, tokenizer):
        # or use the RobertaTokenizer from `transformers` directly.

        self.examples = []
        
        for example in df.values:
            x=tokenizer.encode_plus(example, max_length = MAX_LEN, truncation=True, padding=True)
            self.examples += [x.input_ids]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        # We’ll pad at the batch level.
        return torch.tensor(self.examples[i])


df=pd.concat([train_df['sentence'], test_df['sentence']], axis=0)
#print('Total: ',len(df), len(train_df), len(test_df))
#train_dataset = CustomDataset(train_df['sentence'], tokenizer)

train_dataset = CustomDataset(train_df['sentence'], tokenizer)
eval_dataset = CustomDataset(test_df['sentence'], tokenizer)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

training_args = TrainingArguments(
    output_dir="/out",
    overwrite_output_dir=True,
    evaluation_strategy = 'epoch',
    num_train_epochs=TRAIN_EPOCHS,
    learning_rate=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY,
    per_device_train_batch_size=TRAIN_BATCH_SIZE,
    per_device_eval_batch_size=VALID_BATCH_SIZE,
    save_steps=8192,
    #eval_steps=4096,
    save_total_limit=1,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    #prediction_loss_only=True,
)

trainer.train()
eval_results = trainer.evaluate()
print(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")
trainer.save_model('C:/Users/TIA/Desktop')
