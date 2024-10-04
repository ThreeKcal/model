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
            sql = "SELECT num, comments, request_user, request_time, prediction_result, prediction_score, prediction_time FROM comments WHERE prediction_result IS NULL LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
    print(result)

    if result is None:
        data = {"message":f"❌예측할 모델이 없습니다❌"}
        print(data)
    else:
        num = result['num']
        from threekcal_model.model import prediction
        prediction = prediction(result['comments'])
        print(prediction)
        prediction_result=prediction[0]['label']
        prediction_score =prediction[0]['score']
        prediction_time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        log_data=[num,prediction_result,prediction_score,prediction_time]
    print(log_data)
    return log_data


run()
