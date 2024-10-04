from typing import Union

from fastapi import FastAPI
from transformers import pipeline
from threekcal_model.utils import get_label, get_score

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/comments/")
def read_item(user: str, comments: str):
    #모델 불러오기
    model = pipeline("text-classification", model="michellejieli/emotion_text_classifier")
    
    prediction = model(f"{comments}")

    import pymysql.cursors
    import os
    
    sql = "INSERT INTO comments(`comments`, `request_time`, `request_user`) VALUES(%s,%s,%s)"

    import jigeum.seoul
    from threekcal_model.db import dml
    insert_row = dml(sql, comments, jigeum.seoul.now(), user)
    
    return {
            "comments": comments,
            "request_time": jigeum.seoul.now(),
            "request_user": user, 
            "label": prediction[0]['label'],
            "score": prediction[0]['score']
            }
