import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

st.title('요청자, 처리자간의 통계')

def load_data():
    #url = 'http://43.202.66.118:8077/all'
    #r = requests.get(url)
    #d = r.json()
    d = pd.read_csv("~/Documents/updated_trial.csv")
    return d

data = load_data()
df = pd.DataFrame(data)

st.title("감정 데이터 분석")

st.subheader("최종 데이터")
st.dataframe(df)

st.subheader("예측 결과 확률분포 (?)")
fig, ax = plt.subplots()
sns.countplot(data=df, x='prediction_result', ax=ax)
st.pyplot(fig)

selected_label = st.selectbox("예측결과 선택", df['prediction_result'].unique())
filtered_df = df[df['prediction_result'] == selected_label]

st.write(f"{selected_label}의 필터링된 데이터")
st.dataframe(filtered_df)

st.subheader("Prediction Scores의 분포")
fig, ax = plt.subplots()
sns.histplot(filtered_df['prediction_score'], bins=10, ax=ax)
st.pyplot(fig)

st.subheader("Confusion Matrix & Heatmap")
fig, ax = plt.subplots()

cm = confusion_matrix(df['label'], df['prediction_result'])
unique_labels = df['label'].unique()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
st.pyplot(plt)
