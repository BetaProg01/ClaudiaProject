import torch
from torch.utils.data import DataLoader
from transformers import BertForSequenceClassification, BertTokenizer, AdamW
from restaurantRezviewDataset import RestaurantReviewDataset




def main():
    # Initialisation
    model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'  # Nom du modèle BERT à utiliser
    tokenizer = BertTokenizer.from_pretrained(model_name)  # Initialisation du tokenizer
    model = BertForSequenceClassification.from_pretrained(model_name)  # Initialisation du modèle

    # read comments.txt file
    comments = []
    with open('comments.txt', 'r') as f:
        for line in f:
            comments.append(line.strip())

    # read scores.txt file
    scores = []
    with open('scores.txt', 'r') as f:
        for line in f:
            scores.append(int(line.strip()) - 1)


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




if __name__ == '__main__':
    main()