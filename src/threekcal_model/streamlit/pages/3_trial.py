import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_curve, average_precision_score, classification_report, confusion_matrix
from sklearn.preprocessing import label_binarize
import numpy as np

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

st.subheader("Confusion Matrix & Heatmap")
fig, ax = plt.subplots()

cm = confusion_matrix(df['label'], df['prediction_result'])
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

unique_emotions = df['label'].unique()

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

st.subheader("Classification Report")
report = classification_report(df['label'], df['prediction_result'], target_names=unique_emotions,output_dict=True)
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

st.markdown("### Precision (정밀도)")
st.write("정밀도는 모델이 긍정 클래스(예: 긍정적인 예측)를 예측한 것 중에서 실제로 긍정 클래스인 비율을 나타냅니다.")
st.latex(r"\text{정밀도} = \frac{\text{TP}}{\text{TP} + \text{FP}}")
st.write("여기서 TP는 True Positives(참 긍정), FP는 False Positives(거짓 긍정)을 의미합니다.")

st.markdown("### Recall (재현율)")
st.write("재현율은 실제 긍정 클래스 중에서 모델이 긍정 클래스로 올바르게 예측한 비율을 나타냅니다.")
st.latex(r"\text{재현율} = \frac{\text{TP}}{\text{TP} + \text{FN}}")
st.write("여기서 FN은 False Negatives(거짓 부정)을 의미합니다.")
