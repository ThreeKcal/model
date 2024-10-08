import streamlit as st
import pandas as pd
import requests

st.title('코멘트 & 라벨 적기')

def load_data():
    #url = 'http://127.0.0.1:8000/all'
    url = 'http://54.180.132.11:8001/all'
    r = requests.get(url)
    d = r.json()
    return d

def get_table(num, remark, label):
    data = load_data()
    df = pd.DataFrame(data)
    df = df.head(10)
    none_remark_df = df[df['remark'].isnull()]
    none_remark_df = none_remark_df.reset_index(drop=True)
    html_table = none_remark_df.to_html(index=False)

    styled_html_table = f"""
<style>
    table {{
        width = 60%;
        border-collapse: collapse;
        font-size: 14px;
}}
    th, td {{
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }}
</style>
{html_table}
""" # Streamlit에서 HTML로 출력
    st.write(styled_html_table, unsafe_allow_html=True)

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
    

# page start

num = st.text_input("코멘트 넣고 싶은 줄의 num을 입력해 주세요", "")
remark = st.text_input("결과에 대한 코멘트를 남겨주세요", "")
label = st.text_input("본인이 보기에 해당 입력값의 실제 감정 label은? 정답치로 사용됩니다.", "")

input_label()
get_table(num, remark, label)
