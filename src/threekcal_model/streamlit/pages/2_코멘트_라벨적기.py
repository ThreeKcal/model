import streamlit as st
import pandas as pd
import requests

st.title('요청자, 처리자간의 통계')

def load_data():
    url = 'http://127.0.0.1:8000/all'
    #url = 'http://54.180.132.11:8001/all'
    r = requests.get(url)
    d = r.json()
    return d

def get_table():
    data = load_data()
    df = pd.DataFrame(data)
    df.head(10)
    none_remark_df = df[df['remark'].isnull()]
    none_remark_df = none_remark_df.reset_index(drop=True)
    html_table = none_remark_df.to_html(index=False)
    # Streamlit에서 HTML로 출력
    st.write(html_table, unsafe_allow_html=True)

get_table()

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
                st.write(f"num:{num}에 remark:{remark}와 label:{label}이(가) 업데이트 되었습니다!")
                conn = get_conn()
                with conn.cursor() as cursor:
                    sql = "UPDATE comments SET remark = %s, label = %s WHERE num = %s"
                    cursor.execute(sql, (remark, label, num))

                # 변경 사항 저장 (commit)
                conn.commit()
                st.rerun() 
            else:
                st.write("세 항목을 모두 입력해 주세요.")

    except Exception as e:
        print(f"Error: {e}")
    

input_label()
