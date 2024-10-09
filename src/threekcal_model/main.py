import streamlit as st
import os

st.set_page_config(
    page_title="Three Kcal Team Portfolio",
    page_icon="👋",
)

st.write("#  팀 3kcal 감정 분석 모델 관리 페이지에 오신걸 환영합니다. 👋")

file_path=__file__
image_path=os.path.join(os.path.dirname(file_path),"pages/images/mainpage1.jpg")

st.image(image_path)

st.markdown(
    """
    팀 3kcal 모델 관리 페이지에는 메인 페이지 

    예측 하고싶은 텍스트를 업로드하는 "텍스트 업로드 페이지"   

    예측된 결과값을 바탕으로 코멘트와 라벨을 작성하는 "코멘트 및  라벨적기" 페이지
  
    입력된 데이터를 바탕으로 머신러닝 정답율과 관련 다양한 통계를 볼 수 있는 "결과 통계" 페이지로 구성되어 있습니다.
    
    👋주의 사항!👋 

    텍스트 업로드 페이지를 이용하실때 리뷰 부분은 영어로만 작성해주세요! 
    """
)
