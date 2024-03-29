from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch
from pprint import pprint


def get_model():
    # read model from model folder, containing model.safetensors and config.json
    model = BertForSequenceClassification.from_pretrained('model')
    return model

def sentiment_analysis_over_subject(text, subject, keywords, model_path='nlptown/bert-base-multilingual-uncased-sentiment'):
    # Detect if text contains keywords of subject
    for word in keywords:
      found = word in text
      if found:
        break
      else:
        sentiment_label = -1
        probabilities = []

    # if found:
    tokenizer = BertTokenizer.from_pretrained(model_path)
    # model = BertForSequenceClassification.from_pretrained(model_path)
    model = get_model()

    # Tokenize the input text and subject
    input_text = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    input_subject = tokenizer(subject, return_tensors="pt", truncation=True, padding=True)

    # Concatenate the input_text and input_subject for fine-tuning
    input_combined = {
        'input_ids': torch.cat([input_text['input_ids'], input_subject['input_ids']], dim=1),
        'attention_mask': torch.cat([input_text['attention_mask'], input_subject['attention_mask']], dim=1)
    }

    # Fine-tune the model on your labeled dataset

    # Perform inference
    with torch.no_grad():
        logits = model(**input_combined).logits

    # Apply softmax to get probabilities
    probabilities = softmax(logits, dim=1).squeeze().tolist()

    # Assuming the model is trained for sentiment classes (e.g., negative, neutral, positive)
    sentiment_label = torch.argmax(logits).item()

    return sentiment_label, probabilities


#liste des mots clés
path = "keywords_organic.txt"
keywords = []
with open(path, 'r') as fichier:
    for ligne in fichier.readlines():
      keywords.append(ligne)



# Fonction pour obtenir les notes d'un seul commentaire
def general_labelization_single_review(review, subjects = [ 'Organic' , 'Climate' , 'Water' , 'Social' , 'Governance' , 'Waste' , 'Adverse'], keywords = keywords):
  res = {}
  #pour chaque commentaire fait une analyse de sentiment pour chaque sujet
  for subject in subjects:
      sentiment_label, probabilities = sentiment_analysis_over_subject(review, subject, keywords)
      res[subject] = sentiment_label+1
  return res



## Fonction pour obtenir les notes de plusieurs commentaires
#input -> liste des commentaires a labeliser
#subjects -> liste des sujets predefinis pour l'analyse de sentiments
def general_labelization_multiple_reviews(comments, subjects = [ 'Organic' , 'Climate' , 'Water' , 'Social' , 'Governance' , 'Waste' , 'Adverse'], keywords = keywords):
  res = []
  #pour chaque commentaire fait une analyse de sentiment pour chaque sujet
  for comment in comments:
      sc = general_labelization_single_review(comment, subjects, keywords)
      res.append(sc)
  return res




def main():
  path = 'reviews_organic.txt'
  inputs = []
  with open(path, 'r') as fichier:
      for ligne in fichier.readlines():
        inputs.append(ligne)

  pprint(general_labelization_multiple_reviews(inputs[:10],))



if __name__ == "__main__":
    main()