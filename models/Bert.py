import torch.nn as nn
import torch

class BERT(nn.Module):
    def __init__(self, bert, dropout=0.1):
        super(BERT, self).__init__()
        
        self.bert = bert
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(768, 512)
        self.fc2 = nn.Linear(512, 1)
        self.relu = nn.ReLU()
         
    def forward(self, ids, mask, token_type_ids):
        _, o2= self.bert(ids,attention_mask=mask,token_type_ids=token_type_ids, return_dict=False)
        
        x = self.fc1(o2)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x        
    
class HC3DatasetForBert(torch.utils.data.Dataset):
    def __init__(self, tokenizer, X):
        self.data = X
        self.tokenizer = tokenizer
        self.max_length = 512
    
    def __getitem__(self, idx):
        x = self.data['text'][idx]
        x = self.tokenizer.encode_plus(
            x,
            None,
            padding='max_length',
            add_special_tokens=True,
            return_attention_mask=True,
            max_length=self.max_length,
            truncation=True
        )
        ids = x['input_ids']
        token_type_ids = x['token_type_ids']
        mask = x['attention_mask']
        y = self.data['labels'][idx]
        
        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
            'target': torch.tensor(y, dtype=torch.long)
            }
    
    def __len__(self):
        return len(self.data)
        