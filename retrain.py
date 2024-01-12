import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertForSequenceClassification, BertTokenizer, AdamW

# Initialisation
model_name = 'bert-base-uncased'  # Nom du modèle BERT à utiliser
num_labels = 6  # Les notes vont de 0 à 5, donc nous avons 6 labels possibles
tokenizer = BertTokenizer.from_pretrained(model_name)  # Initialisation du tokenizer
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)  # Initialisation du modèle



# read comments.txt file
comments = []
with open('comments.txt', 'r') as f:
    for line in f:
        comments.append(line.strip())

# read scores.txt file
scores = []
with open('scores.txt', 'r') as f:
    for line in f:
        scores.append(int(line.strip()))

print("Nombre de commentaires:", len(comments))
print("Nombre de notes:", len(scores))


# Préparation des données
class RestaurantReviewDataset(Dataset):
    def __init__(self, comments, scores, tokenizer):
        self.comments = comments  # Commentaires du restaurant
        self.scores = scores  # Notes correspondantes
        self.tokenizer = tokenizer  # Tokenizer à utiliser

    def __len__(self):
        return len(self.comments)  # Retourne le nombre total de commentaires

    def __getitem__(self, idx):
        comment = self.comments[idx]  # Récupère le commentaire à l'index idx
        score = self.scores[idx]  # Récupère la note correspondante
        encoding = self.tokenizer.encode_plus(
            comment,
            truncation=True,  # Tronque le commentaire si nécessaire
            padding='max_length',  # Remplit le commentaire jusqu'à la longueur maximale
            max_length=128,  # Longueur maximale pour les séquences d'entrée
            return_tensors='pt'  # Retourne des tenseurs PyTorch
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),  # IDs d'entrée pour le modèle BERT
            'attention_mask': encoding['attention_mask'].flatten(),  # Masque d'attention pour le modèle BERT
            'labels': torch.tensor(score, dtype=torch.long)  # Convertit la note en tensor PyTorch
        }

# Création du DataLoader
dataset = RestaurantReviewDataset(comments, scores, tokenizer)  # Crée un jeu de données à partir des commentaires et des notes
dataloader = DataLoader(dataset, batch_size=16)  # Crée un DataLoader pour itérer sur le jeu de données

# Entraînement du modèle
optimizer = AdamW(model.parameters(), lr=1e-5)  # Initialise l'optimiseur
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')  # Utilise le GPU si disponible, sinon le CPU
model.to(device)  # Déplace le modèle vers le périphérique choisi

for epoch in range(10):  # Boucle sur les époques (vous pouvez ajuster ce nombre)
    for batch in dataloader:  # Boucle sur les lots de données
        input_ids = batch['input_ids'].to(device)  # Récupère les IDs d'entrée
        attention_mask = batch['attention_mask'].to(device)  # Récupère le masque d'attention
        labels = batch['labels'].to(device)  # Récupère les labels

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)  # Passe les données à travers le modèle
        loss = outputs.loss  # Récupère la perte
        loss.backward()  # Calcule les gradients

        optimizer.step()  # Met à jour les poids du modèle
        optimizer.zero_grad()  # Réinitialise les gradients
        print("Loss:", loss.item())

print("L'entraînement est terminé.")  # Affiche un message lorsque l'entraînement est terminé
model.save_pretrained('model')