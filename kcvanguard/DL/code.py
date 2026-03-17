import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModel
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import re

# 1. LEETSPEAK NORMALIZATION
def clean_toxic_text(text):
    text = str(text).lower()
    replacements = {
        '3': 'e', '1': 'i', '0': 'o', '4': 'a', '5': 's', 
        '7': 't', '$': 's', '@': 'a', '8': 'b', 'x': 'x'
    }
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    text = re.sub(r'([!?.])\1+', r'\1', text) 
    return text.strip()

# 2. UPDATED DATASET CLASS (Fixes the AttributeError)
class ToxicDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        # Ensure text is a string to avoid tokenizer errors
        text = str(self.texts[item])
        
        # Using the direct __call__ method instead of encode_plus for maximum compatibility
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )
        
        return {
            'ids': encoding['input_ids'].flatten(),
            'mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[item], dtype=torch.long)
        }

# 3. WINNER'S ARCHITECTURE: TRANSFORMER + BI-GRU
class ToxicClassifier(nn.Module):
    def __init__(self, n_classes):
        super(ToxicClassifier, self).__init__()
        self.bert = AutoModel.from_pretrained('bert-base-uncased')
        self.gru = nn.GRU(768, 256, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.3)
        self.out = nn.Linear(512, n_classes)

    def forward(self, ids, mask):
        outputs = self.bert(input_ids=ids, attention_mask=mask)
        # Sequence output for GRU
        last_hidden_state = outputs.last_hidden_state 
        
        gru_out, _ = self.gru(last_hidden_state)
        
        # Max pooling across sequence as per winner strategy
        pooled_output, _ = torch.max(gru_out, dim=1)
        
        output = self.dropout(pooled_output)
        return self.out(output)

# 4. ROBUST TRAINING ENGINE
def train_model():
    df = pd.read_csv('/kaggle/input/competitions/dl-assignment-toxic-comment-classification/train.csv')
    df['Toxic Comment'] = df['Toxic Comment'].apply(clean_toxic_text)
    
    label_map = {"Insult": 0, "Threat": 1, "Sexual Harassment": 2}
    inv_label_map = {v: k for k, v in label_map.items()}
    df['label'] = df['Classification'].map(label_map)

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['Toxic Comment'].values, df['label'].values, test_size=0.15, random_state=42
    )

    # Initialize Tokenizer
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    
    # Create DataLoaders
    train_loader = DataLoader(ToxicDataset(train_texts, train_labels, tokenizer, 80), batch_size=16, shuffle=True)
    val_loader = DataLoader(ToxicDataset(val_texts, val_labels, tokenizer, 80), batch_size=16)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ToxicClassifier(n_classes=3).to(device)
    
    # Optimized Optimizer settings
    optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=1e-6)
    loss_fn = nn.CrossEntropyLoss().to(device)

    print(f"Training on: {device}")
    for epoch in range(3):
        model.train()
        total_loss = 0
        for batch in train_loader:
            ids = batch['ids'].to(device)
            mask = batch['mask'].to(device)
            labels = batch['labels'].to(device)

            optimizer.zero_grad()
            outputs = model(ids, mask)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # Validation Logic
        model.eval()
        preds_list, labels_list = [], []
        with torch.no_grad():
            for batch in val_loader:
                ids = batch['ids'].to(device)
                mask = batch['mask'].to(device)
                outputs = model(ids, mask)
                _, preds = torch.max(outputs, dim=1)
                preds_list.extend(preds.cpu().numpy())
                labels_list.extend(batch['labels'].numpy())
        
        val_acc = accuracy_score(labels_list, preds_list)
        print(f"Epoch {epoch+1} | Loss: {total_loss/len(train_loader):.4f} | Val Acc: {val_acc:.4f}")

    return model, tokenizer, device, inv_label_map

# 5. EXECUTION
if __name__ == "__main__":
    
    # Train model
    trained_model, tokenizer, device, inv_map = train_model()
    trained_model.eval()

    # Load test.csv
    test_df = pd.read_csv("/kaggle/input/competitions/dl-assignment-toxic-comment-classification/test.csv")
    test_ids = test_df["id"].tolist()
    test_texts = test_df["Toxic Comment"].tolist()

    predictions = []

    with torch.no_grad():
        for text in test_texts:
            clean = clean_toxic_text(text)

            enc = tokenizer(
                clean,
                return_tensors='pt',
                max_length=80,
                truncation=True,
                padding='max_length'
            )

            ids = enc['input_ids'].to(device)
            mask = enc['attention_mask'].to(device)

            out = trained_model(ids, mask)

            _, pred = torch.max(out, dim=1)

            predictions.append(inv_map[pred.item()])

    # Create submission
    submission = pd.DataFrame({
        "id": test_ids,
        "Classification": predictions
    })

    submission.to_csv("submission.csv", index=False)
    print("Submission saved as submission.csv")