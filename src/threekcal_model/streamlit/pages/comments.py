import streamlit as st
import requests
import json

user = st.text_input("유저ID", "")
title = st.text_input("리뷰", "")

def load_data():
    if user and title is not None:
        headers = {
                    'accept': 'application/json',
                    }

        params = {
                    'user': f'{user}',
                    'comments': f'{title}',
}

        response = requests.get('http://127.0.0.1:8000/comments/', params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            label = data['label']
            score = data['score']
            st.write(f"{user}의 기분은...?", f"{label}, 감정의 정확도는 {score}")

load_data()
