from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn as nn
  
tokenizer = AutoTokenizer.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")

model = AutoModelForSequenceClassification.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")

emotions_map = {
    "0": "admiration",
    "1": "amusement",
    "2": "anger",
    "3": "annoyance",
    "4": "approval",
    "5": "caring",
    "6": "confusion",
    "7": "curiosity",
    "8": "desire",
    "9": "disappointment",
    "10": "disapproval",
    "11": "disgust",
    "12": "embarrassment",
    "13": "excitement",
    "14": "fear",
    "15": "gratitude",
    "16": "grief",
    "17": "joy",
    "18": "love",
    "19": "nervousness",
    "20": "optimism",
    "21": "pride",
    "22": "realization",
    "23": "relief",
    "24": "remorse",
    "25": "sadness",
    "26": "surprise",
    "27": "neutral"
}

def calculate_emotions(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    emotions = nn.functional.softmax(outputs.logits, dim=1).view(28)
    return emotions

def create_emotions_list(model_outputs, label_obj):
    labels = [e for e in label_obj.values()]
    scores = [round(float(o), 3) for o in model_outputs]
    emotions_list = []
    for l, s in zip(labels, scores):
        d = {}
        d['label'], d['score'] = l, s
        emotions_list.append(d)
    return emotions_list

def query(text):
    raw_e = calculate_emotions(text)
    list_of_emotions = create_emotions_list(raw_e, emotions_map)

    return list_of_emotions

#TODO decide whether or not to accept sentences and do inference inside of function or only accept the argument already in inference form
def generate_report(e_scores):
    filtered_emotions = [o for o in e_scores if o['score'] > 0.03]
    for e in filtered_emotions:
        label, score = e['label'], e['score']
        print(f'{label:<15} {score:>.4f}')
    print('\n')
    print('\n')