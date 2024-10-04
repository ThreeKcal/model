from typing import Union

from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/comments/")
def read_item(comments: str):
    #모델 불러오기
    model = pipeline("text-classification", model="michellejieli/emotion_text_classifier")
    
    prediction = model(f"{comments}")
    return {"result": prediction}
