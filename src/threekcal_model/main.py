from typing import Annotated
from fastapi import FastAPI, File
import os
import pymysql.cursors

app = FastAPI()

@app.post("/")
def read_root():
    return {"Hello": "World!"}

@app.get("/input")
def semtiment(input_str="Great!"):
    prediction = ""
    # Use a pipeline as a high-level helper
    from transformers import pipeline
    pipe = pipeline("text-classification", model="michellejieli/emotion_text_classifier")

    prediction = pipe(input_str)
# TODO: implement model call

    return { "input": input_str, "prediction": prediction }
