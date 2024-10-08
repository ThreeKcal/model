import streamlit as st
import pandas as pd
import requests

st.title('결과 통계')
AWS_URL = 'http://54.180.132.11:8001/'
LOCAL_URL = 'http://127.0.0.1:8000/'

def load_data():
    url = ''.join([AWS_URL, 'all'])
    r = requests.get(url)
    d = r.json()
    return d
d=load_data()
df = pd.DataFrame(d)
df
def show_stats():
    pass


# page start

#data = load_data()
#df = pd.DataFrame(data)

st.write("현재까지의 모델 결과 통계입니다.")
