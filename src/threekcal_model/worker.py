import random
import os
import requests
from datetime import datetime
from pytz import timezone
import pymysql.cursors
from threekcal_model.db import get_connection


def run():
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT num,comments, request_user, request_time, prediction_result, prediction_score, prediction_time WHERE prediction_result IS NULL LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()

    if result is None:
        data = {"message":f"❌예측할 모델이 없습니다❌"}
        print(data)
    else:
        num = result['num']
        from threekcal_model.model import prediction
        prediction = prediction()
        prediction_result=prediction['label']
        prediction_score =prediction['score']
        prediction_time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = """UPDATE comments
                         SET prediction_result=%s,
                             prediction_score=%s,
                             prediction_time=%s
                         WHERE num = %s"""
                cursor.execute(sql,(prediction_result, prediction_score, prediction_time, num))
                connection.commit()
    data = {f"prediction_result:{prediction_result}, prediction_score:{prediction_score}"}
    print(response.text)
    print(data)
    return True
    
