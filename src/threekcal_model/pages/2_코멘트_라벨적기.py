import streamlit as st
import pandas as pd
import requests
from requests.exceptions import ConnectionError, RequestException

st.title('코멘트 & 라벨 적기')

def load_data():
    #url = 'http://127.0.0.1:8000/all'
    url = 'http://54.180.132.11:8001/all'
    try:
        r = requests.get(url)
        d = r.json()
        return d

    except ConnectionError:
        # 열 이름 리스트
        columns = ['num', 'comments', 'request_time', 'request_user', 'prediction_result', 'prediction_score', 'prediction_time', 'remark', 'label']

        # 빈 데이터프레임 생성
        df = pd.DataFrame(columns=columns)
        st.write(df)
        return None

# request_user 선택
def select_request_user(unique_id):
    data = load_data()
    df = pd.DataFrame(data)

    # "모든 사용자" 옵션 추가
    options = ["모든 사용자"] + df['request_user'].unique().tolist()

    # 사용자 선택
    user = st.selectbox(
        "request user 선택",
        options,
        index=0,  # 기본값은 "모든 사용자"
        placeholder="request_user를 선택해주세요.",
        key=f"select_request_user_{unique_id}"  # 고유한 key 값 설정
    )

    return user

# 선택된 사용자에 따라 num 선택 필터링
def select_num(user, unique_id):
    data = load_data()
    df = pd.DataFrame(data)
    df = df[df['remark'].isnull()]
    # 선택된 user에 따라 num 값을 필터링
    if user != "모든 사용자":
        filtered_df = df[df['request_user'] == user]
        options = ["모든 번호"] + filtered_df['num'].unique().tolist()
    else:
        options = ["모든 번호"] + df['num'].unique().tolist()  # 전체 번호 표시

    # num 선택
    num_option = st.selectbox(
        "num 선택",
        options,
        index=0,
        placeholder="num을 선택해주세요.",
        key=f"select_num_{unique_id}"  # 고유한 key 값 설정
    )

    return num_option

# 테이블을 필터링하여 보여주는 함수
def show_table(user, unique_id):
    data = load_data()
    df = pd.DataFrame(data)

    # 'remark'가 null인 데이터만 필터링
    df = df[df['remark'].isnull()]

    # 사용자가 선택한 user와 num에 따라 데이터 필터링
    if user != "모든 사용자":
        df = df[df['request_user'] == user]

    #if num != "모든 번호":
    #    df = df[df['num'] == num]

    # 필터링된 테이블 출력
    if not df.empty:
        st.write(df)
    else:
        st.write("선택한 조건에 맞는 데이터가 없습니다.")

# 데이터 업데이트하는 함수 (num 필드를 사용하여 업데이트)
def input_label(user, num):
    import pymysql.cursors
    import os
    from threekcal_model.db import get_conn

    # remark와 label 입력을 위한 text input
    remark = st.text_input("결과에 대한 코멘트를 남겨주세요", key="remark_input_key")
    label = st.text_input("본인이 보기에 해당 입력값의 실제 감정 label은?", key="label_input_key")

    try:
        if st.button("Submit", key="submit_button_key"):
            if remark and label and num != "모든 번호":
                st.write(f"num: {num}, 사용자: {user}에 대한 remark: {remark}와 label: {label}이(가) 업데이트 되었습니다!")
                conn = get_conn()
                with conn.cursor() as cursor:
                    # SQL 업데이트 쿼리 실행 (num 기준으로 업데이트)
                    sql = "UPDATE comments SET remark = %s, label = %s WHERE num = %s"
                    cursor.execute(sql, (remark, label, num))

                # 변경 사항 저장 (commit)
                conn.commit()
                st.rerun()  # 페이지 리로드
            else:
                st.write("모든 항목을 입력해 주세요.")
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit 애플리케이션 실행
try:
    if __name__ == "__main__":
        # 고유한 키 식별자를 사용하여 사용자와 num을 선택
        selected_user = select_request_user("user_table_1")
        selected_num = select_num(selected_user, "num_table_1")

        # 선택한 값에 맞는 테이블을 보여줌
        show_table(selected_user, "table_1")

        # 데이터를 업데이트하는 입력 부분 (num 필드 포함)
        input_label(selected_user, selected_num)

except Exception as e:
    st.error("서버가 불안정하여 DB에 연결할 수 없습니다. 나중에 다시 시도해주세요.")
