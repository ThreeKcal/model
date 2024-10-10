import streamlit as st
import requests
import json
import pandas as pd 

user = st.text_input("유저ID", "")
title = st.text_input("리뷰", "")

def load_data():
    if st.button("Submit"):
        if user and title:
            headers = {'accept': 'application/json',}
            params = {'user': f'{user}', 'comments': f'{title}'}
            
            try:
                response = requests.get('http://54.180.132.11:8001/comments/', params=params, headers=headers,timeout=7)

                if response.status_code == 200:
                    st.write(f"유저ID [{user}]의 리뷰 \"{title}\"가 성공적으로 업로드 되었습니다!")
                    url = 'http://54.180.132.11:8001/all'
                    r = requests.get(url)
                    d = r.json()
                    df = pd.DataFrame(d)
                    st.dataframe(df.tail(5))
                    st.write(f"모델에 따른 감정 예측은 이후 airflow를 통해 순차적으로 진행됩니다. 좌측의 \"코멘트 라벨적기\" 페이지를 통해 개별 결과 확인 및 피드백을, \"결과 통계\" 페이지를 통해 전체적인 모델 API의 성능 통계를 확인할 수 있습니다.")
                else: 
                    st.write("Something went wrong!")
            except Exception as e:
                st.write("서버가 불안정하여 DB에 연결할 수 없습니다. 나중에 다시 시도해주세요.")

        else:
            st.write("두 항목을 모두 입력해 주세요.")
        #    data = response.json()
        #    label = data['label']
        #    score = data['score']
        #    st.write(f"{user}의 기분은...?", f"{label}, 감정의 정확도는 {score}")

load_data()
