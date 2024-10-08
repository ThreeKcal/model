from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/comments/")
def read_item(user: str, comments: str):

    #DB에 저장하기
    import pymysql.cursors
    import os
    
    sql = "INSERT INTO comments(`comments`, `request_time`, `request_user`) VALUES(%s,%s,%s)"

    import jigeum.seoul
    from threekcal_model.db import dml
    insert_row = dml(sql, comments, jigeum.seoul.now(), user)

    #출력값
    return {
            "comments": comments,
            "request_time": jigeum.seoul.now(),
            "request_user": user, 
            }

@app.get("/all/")
def read_item():
    from threekcal_model.db import get_conn
    conn = get_conn()

    with conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM comments"
            cursor.execute(sql)
            result = cursor.fetchall()

    return result
