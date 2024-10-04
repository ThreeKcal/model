#이것은 사용중이지 않은 코드입니다!!!!!

import requests
import os
from threekcal_model.db import select, dml

def get_job_task():
    sql = """
    SELECT num, comments, request_time, request_user
    FROM comments
    WHERE prediction_result IS NULL
    ORDER BY num -- 가장 오래된 요청
    LIMIT 1 -- 하나씩
    """
    r = select(sql, 1)

    print("===="*33)
    print(f'r = {r}')

    if len(r) > 0:
        return r[0]
    else:
        return None

def prediction(file_path, num):
    sql = """UPDATE comments
    SET prediction_result=%s,
        prediction_time=%s,
        prediction_time=%s
    WHERE num=%s
    """
    presult = predict_digit(file_path)
    dml(sql, presult, model_name, jigeum.seoul.now(), num)

    return presult

def run():
    """comments 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""

    job = get_job_img_task()

    if job is None:
      print(f"{jigeum.seoul.now()} - job is None")
      return

    num = job['num']
    file_name = job['file_name']
    file_path = job['file_path']

    presult = prediction(file_path, num)
    print(jigeum.seoul.now())
