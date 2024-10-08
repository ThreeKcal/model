import streamlit as st
import pandas as pd
import requests
import numpy as np
import pymysql.cursors
import os
from threekcal_model.db import get_conn

st.title('요청자, 처리자간의 통계')

def load_data():
    url = 'http://54.180.132.11:8001/all'
    r = requests.get(url)
    d = r.json()
    return d

data = load_data()
df = pd.DataFrame(data)
nulldf = df[(df['label'].isnull()) | (df['remark'].isnull())]
#st.write(df[(df['label'].isnull()) | (df['remark'].isnull())])
selected=df['request_user'].unique()
selected=np.append(selected,"없음")
selected_label = st.selectbox("입력 유저 선택", selected)

if selected_label == "없음":
    st.write(nulldf)
else :
    filtered_df = nulldf[nulldf['request_user']== selected_label]
    st.write(f"{selected_label}의 필터링된 데이터")
    st.dataframe(filtered_df)

#num = st.text_input("num", "")
#remark = st.text_input("의견을 남겨주세요", "")
#label = st.text_input("정답", "")
options = ["angry","disgust","fear","joy","neutral","sadness","surprise"]


with st.form("내 폼",clear_on_submit=True):
    num = st.text_input("숫자")
    label = st.selectbox("label을 설정하세요", options)
    remark = st.text_input("코멘트")
    submit_button = st.form_submit_button(label="제출")

    if submit_button:
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
        st.write("제출되었습니다! 감사합니다!")
    

#def input_label():
#    import pymysql.cursors
#    import os
#    from threekcal_model.db import get_conn
#    try:
#        if st.button("Submit"):
#            if remark and label and num:
#                st.write(f"{num}에 {remark}와 {label}이(가) 업데이트 되었습니다!")
#                conn = get_conn()
#                with conn.cursor() as cursor:
#                    sql = "UPDATE comments SET remark = %s, label = %s WHERE num = %s"
#                    cursor.execute(sql, (remark, label, num))

                # 변경 사항 저장 (commit)
#                conn.commit()

#            else:
#                st.write("세 항목을 모두 입력해 주세요.")

#   except Exception as e:
#        print(f"Error: {e}")

# input_label()
