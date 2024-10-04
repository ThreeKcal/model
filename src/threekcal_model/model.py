from transformers import pipeline
model = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")

def prediction(text : str):
    return model(text)

