import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.title('3kcal 텍스트 감정 분류 예측 관제 시스템')

st.markdown('### 페이지 별 기능 설명')

st.markdown('#### 1.text_upload : 텍스트를 입력해서 DB에 저장하는 페이지')

st.markdown('#### 2.input_comment_and_label.py : 잘못 예측한 comment에 대해서 remark와 label을 달아주는 페이지'
)
    
st.markdown('#### 3.result_statistic.py : 예측에 대해서 정오답에 대한 통계를 보여주는 페이지') 
