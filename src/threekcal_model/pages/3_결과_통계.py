import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_curve, average_precision_score, classification_report, confusion_matrix
from sklearn.preprocessing import label_binarize
import numpy as np
import random


def load_data():
    url = 'http://54.180.132.11:8001/all'
    r = requests.get(url)
    d = r.json()
    return d

data = load_data()
df = pd.DataFrame(data)

st.title("감정 데이터 분석")

st.subheader("최종 데이터")
st.dataframe(df)

st.subheader("Confusion Matrix & Heatmap")
fig, ax = plt.subplots()

# 혼동행렬: 실제값의 범주에 속해있는 데이터의 개수와 예측한 정답의 정오답 개수를 나타낸 표 
cm = confusion_matrix(df[df['label'].notnull()]['label'],df[df['label'].notnull()]['prediction_result'])
unique_labels = df['label'].unique()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
for i in range(cm.shape[0]):
    plt.text(i+0.5, i+0.5, cm[i, i], ha='center', va='center', color='red', fontsize=12, fontweight='bold')

plt.show()
st.pyplot(plt)

selected_label = st.selectbox("예측결과 선택", df['prediction_result'].unique())

st.subheader(f"{selected_label}의 Prediction Scores의 분포")
st.write(f"{selected_label}의 필터링된 데이터")
filtered_df = df[df['prediction_result'] == selected_label]
# st.write(filtered_df['prediction_score'].dtype) /object
filtered_df['prediction_score']=filtered_df['prediction_score'].astype(float)


st.dataframe(filtered_df)

fig, ax = plt.subplots()
bins = np.arange(0, 1.1, 0.1)
sns.histplot(filtered_df['prediction_score'], bins=bins, ax=ax)
st.pyplot(fig)

st.subheader("Density Plot of Prediction Scores")
fig, ax = plt.subplots()
sns.kdeplot(filtered_df['prediction_score'], ax=ax, fill=True)
ax.set_xlim(0, 1)
ax.set_title("Density Plot of Prediction Scores")
ax.set_xlabel("Prediction Score")
ax.set_ylabel("Density")
st.pyplot(fig)

st.subheader("감정마다 Confusion Matrix")
unique_emotions = df[df['label'].notnull()]['label'].unique()

num_emotions = len(unique_emotions)
fig, axes = plt.subplots(nrows=1, ncols=num_emotions, figsize=(6 * num_emotions, 5))

for i, emotion in enumerate(unique_emotions):
    # Create binary columns: 1 if the emotion matches, 0 otherwise
    true_labels = (df['label'] == emotion).astype(int)
    predicted_labels = (df['prediction_result'] == emotion).astype(int)
    cm = confusion_matrix(true_labels, predicted_labels)
    cm_ratio = cm.astype('float') / cm.sum()
    sns.heatmap(cm_ratio, annot=True, fmt='.2%', cmap='Blues', cbar=False,
                ax=axes[i],  # Use the correct subplot
                xticklabels=['Not ' + emotion, emotion],
                yticklabels=['Not ' + emotion, emotion],
                linewidths=1, linecolor='black', annot_kws={"size": 12})

    axes[i].set_xlabel('Predicted')
    axes[i].set_ylabel('Actual')
    axes[i].set_title(f'{emotion} Confusion Matrix')

plt.tight_layout()
plt.show()
st.pyplot(plt)

# 실제 값 y_true, 예측 값 y_pred 감정 클래스 개수 차이 오류
  
lnum=len(df[df['label'].notnull()]['label'].unique())  # 출력 5
pnum=len(df[df['label'].notnull()]['prediction_result'].unique())  # 출력 7 
#st.write(lnum)
#st.write(pnum)


# 해결 방법 1 
# 정확도에 집중한 지표이기 때문에 클래스의 개수가 차이가 나는경우 실제 라벨과 다른 예측값에는 실제 라벨에 있는 클래스 중 랜덤으로 실제 라벨값을 제외한 다른 값으로 예측값을 대체 
if lnum !=  pnum:
    st.write("실제값과 예측값의 클래스 개수의 차이가 있습니다.")
    uq_label_list=np.array(list(unique_emotions))
    tdf = df.copy()
    # 예측된 값이 현재 라벨에 존재하는 클래스가 아닌 클래스로  예측된 경우 
    # st.write(tdf.loc[(tdf['label'].notnull())&(~tdf['prediction_result'].isin(df['label']))]['prediction_result'])
    # 필터링된 데이터 열에 대해서 uq_label_list 중 자기 자신의 label을 제외한 값중 랜덤으로 prediction_score 값을 바꿔주는코드   
    tdf.loc[(tdf['label'].notnull())&(~tdf['prediction_result'].isin(df['label'])),'prediction_result']=tdf[(tdf['label'].notnull())&(~tdf['prediction_result'].isin(df['label']))]['prediction_result'].apply(lambda x : random.choice(uq_label_list[uq_label_list !=x])) 
    #st.write(tdf[(tdf['label'].notnull())&(~tdf['prediction_result'].isin(df['label']))]['prediction_result'])   

    y_real = tdf[tdf['label'].notnull()]['label']
    y_pred = tdf[tdf['label'].notnull()]['prediction_result']
    st.subheader("Classification Report")
    report = classification_report(y_real,y_pred, target_names=unique_emotions,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.table(report_df)

    st.subheader("Precision, Recall, and F1-Score for Each Emotion")
    metrics_df = report_df.iloc[:-3, :-1]
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics_df[['precision', 'recall', 'f1-score']].plot(kind='bar', ax=ax)
    ax.set_title("Classification Metrics by Emotion")
    ax.set_ylabel("Score")
    ax.set_xlabel("Emotion")
    ax.set_xticklabels(metrics_df.index, rotation=45)
    plt.ylim(0, 1)
    st.pyplot(plt)
    
else :
    st.write("실제값과 예측값의 클래스 개수의 차이가 없습니다")
    # 해결 방법 2 
    # label에 있는 값에 대해서만 예측  
    # 개수의 차이가 없다면 그냥 하면되지만 혹시 몰라서 사용
    y_real=df[(df['label'].notnull())&(df['prediction_result'].isin(df['label']))]['label']
    y_pred=df[(df['label'].notnull())&(df['prediction_result'].isin(df['label']))]['prediction_result']
     
    st.subheader("Classification Report")
    report = classification_report(y_real,y_pred, target_names=unique_emotions,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.table(report_df)

    st.subheader("Precision, Recall, and F1-Score for Each Emotion")
    metrics_df = report_df.iloc[:-3, :-1]
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics_df[['precision', 'recall', 'f1-score']].plot(kind='bar', ax=ax)
    ax.set_title("Classification Metrics by Emotion")
    ax.set_ylabel("Score")
    ax.set_xlabel("Emotion")
    ax.set_xticklabels(metrics_df.index, rotation=45)
    plt.ylim(0, 1)
    st.pyplot(plt)


# 조건없는 코드 
#st.subheader("Classification Report")
#report = classification_report(y_real,y_pred, target_names=unique_emotions,output_dict=True)
#report_df = pd.DataFrame(report).transpose()
#st.table(report_df)


st.markdown("### Precision (정밀도)")
st.write("정밀도는 모델이 긍정 클래스(예: 긍정적인 예측)를 예측한 것 중에서 실제로 긍정 클래스인 비율을 나타냅니다.")
st.latex(r"\text{정밀도} = \frac{\text{TP}}{\text{TP} + \text{FP}}")
st.write("여기서 TP는 True Positives(참 긍정), FP는 False Positives(거짓 긍정)을 의미합니다.")

st.markdown("### Recall (재현율)")
st.write("재현율은 실제 긍정 클래스 중에서 모델이 긍정 클래스로 올바르게 예측한 비율을 나타냅니다.")
st.latex(r"\text{재현율} = \frac{\text{TP}}{\text{TP} + \text{FN}}")
st.write("여기서 FN은 False Negatives(거짓 부정)을 의미합니다.")

# ROC curve 
# 사용할 수 없는 이유와 사용하는 방법 
# ROC curve를 사용하려면 prediction_score를 가져올 때 모든 감정 카테고리별 예측 가능도 점수를 가져와야 함 y_true에 값에는 실제 레이블 값에 대하여 encoder로 fit 한 더미변수 y_pred에는y_true 행의 값마다 카테고리별 속할 확률이 적혀 있어야 함 현재 데이터셋으로는 불가능 
