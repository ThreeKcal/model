import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.title('요청자, 처리자간의 통계')

def load_data():
    url = 'http://43.202.66.118:8077/all'
    r = requests.get(url)
    d = r.json()
    return d

data = load_data()
df = pd.DataFrame(data)
