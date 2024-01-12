from torch.utils.data import Dataset
import torch




# Classe pour la préparation des données
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
