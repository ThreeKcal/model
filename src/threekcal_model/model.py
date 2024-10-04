from transformers import pipeline
model = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")

def prediction(text : str):
    a=model(text)
    print(a)
    return a

