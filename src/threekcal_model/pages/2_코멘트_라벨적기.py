import streamlit as st
import pandas as pd
import requests
import numpy as np

st.title('요청자, 처리자간의 통계')

def load_data():
    url = 'http://54.180.132.11:8001/all'
    r = requests.get(url)
    d = r.json()
    return d

data = load_data()
df = pd.DataFrame(data)
#st.write(df[(df['label'].isnull()) | (df['remark'].isnull())])
selected=df['request_user'].unique()
selected=np.append(selected,"없음")
selected_label = st.selectbox("입력 유저 선택", selected)
if selected_label == "없음":
    st.write(st.write(df[(df['label'].isnull()) | (df['remark'].isnull())]))
else :
    filtered_df = df[df['request_user'] == selected_label]
st.write(f"{selected_label}의 필터링된 데이터")
st.dataframe(filtered_df)

num = st.text_input("num", "")
remark = st.text_input("의견을 남겨주세요", "")
label = st.text_input("정답", "")

def input_label():
    import pymysql.cursors
    import os
    from threekcal_model.db import get_conn
    try:
        if st.button("Submit"):
            if remark and label and num:
                st.write(f"{num}에 {remark}와 {label}이(가) 업데이트 되었습니다!")
                conn = get_conn()
                with conn.cursor() as cursor:
                    sql = "UPDATE comments SET remark = %s, label = %s WHERE num = %s"
                    cursor.execute(sql, (remark, label, num))

                # 변경 사항 저장 (commit)
                conn.commit()

            else:
                st.write("세 항목을 모두 입력해 주세요.")

    except Exception as e:
        print(f"Error: {e}")

input_label()
