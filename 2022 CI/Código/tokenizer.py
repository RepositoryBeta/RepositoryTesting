from tokenizers import ByteLevelBPETokenizer

path = "C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA/CLexIS2_single_train.xlsx"

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(files=path,
                vocab_size=50265,
                min_frequency=2,
                special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"])

# Save files to disk
tokenizer.save("models/MarIA")