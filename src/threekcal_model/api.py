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
    
    #모델 입히기
    prediction = model(f"{comments}")

    #DB에 저장하기
    import pymysql.cursors
    import os
    
    sql = "INSERT INTO comments(`comments`, `request_time`, `request_user`) VALUES(%s,%s,%s)"

    import jigeum.seoul
    from threekcal_model.db import dml
    insert_row = dml(sql, comments, jigeum.seoul.now(), user)
    label = get_label(prediction)
    score = get_score(prediction)


    #출력값
    return {
            "comments": comments,
            "request_time": jigeum.seoul.now(),
            "request_user": user, 
            "label": label,
            "score": score
            }
