from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax as softmax 
  
tokenizer = AutoTokenizer.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")

model = AutoModelForSequenceClassification.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")

labels = ["admiration","amusement","anger","annoyance","approval","caring","confusion","curiosity","desire","disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"
]

def calculate_emotions(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    emotions = softmax(outputs.logits, dim=1)
    return emotions

def create_emotions_list(model_outputs, label_obj):
    emotions_sentences = []
    for sentence_output in model_outputs:
        emotions_sentence = []
        for label, score in zip(labels, sentence_output):
            emotions_sentence.append({'label': label, 'score': float(score)})
        emotions_sentences.append(emotions_sentence)
    return emotions_sentences

def query(sentences):
    if sentences == []:
        return []
    outputs = calculate_emotions(sentences)
    sentences_emotions = create_emotions_list(outputs, labels)

    return sentences_emotions
