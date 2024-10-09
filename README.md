# model
## Overview
ML 어플리케이션 서비스를 위한 기본 리포지토리

팀 프로젝트 #3: 팀 ThreeKcal

`DistilRoBERTa` 기반의 text classifier 모델인 [michellejieli/emotion_text_classifier](https://huggingface.co/michellejieli/emotion_text_classifier) 을 통해:
- `Streamlit` 기반 웹 어플리케이션을 통해 사용자 입력을 받고, 해당 문장에 대한 sentiment analysis/prediction 실행 (🤬🤢😀😐😭😲)
- 해당 prediction에 대해 실제 sentiment label 및 피드백 코멘트 역시 입력
- Airflow 부분을 더 알고 싶다면 [이 리포지토리](https://github.com/ThreeKcal/dags/tree/main) 확인
- Pyspark 부분을 더 알고 싶다면 [이 리포지토리](https://github.com/ThreeKcal/pyspark/tree/main)  확인


## Features
### `streamlit` [어플리케이션](http://54.180.132.11:8002/) 시연 모습
- `텍스트 업로드` 페이지: 이용자가 `username`과 `comment`를 입력해 데이터베이스로 전송시킵니다
![text_uploadpage](https://github.com/user-attachments/assets/1099ff86-8491-4002-b375-5f0dbe3e8bfc)

- `코멘트 라벨` 페이지: 전체 혹은 `username` 기준으로 추려낸 코멘트에 관리자가 실제 `label` 값 및 추가 사항을 입력할 수 있습니다
![commentlabelpage](https://github.com/user-attachments/assets/b2c8be3b-54a2-4366-bcf9-5943f40c5569)

- `결과 통계` 페이지: 위 두 페이지를 통해 형성된 데이터베이스에 대한 각종 통계 자료를 볼 수 있습니다. 새로고침할 때마다 새롭게 변경사항을 반영합니다.
![statistic_dynamic](https://github.com/user-attachments/assets/a4f7656e-9a57-46e8-a85b-e6be9c187305)


### Structure
![Blank_diagram_-_Page_1_2](https://github.com/user-attachments/assets/2c2cfbd5-fa7e-4cee-858b-57ccb84e6715)

본 어플리케이션은 `fastapi`와 `airflow`, `maradb`, `pyspark`를 필요로 하는 `streamlit` 웹 어플리케이션입니다.

사용자가 텍스트 업로드 페이지로부터 보낸 입력은 `streamlit`에서 `fastapi`로 전달되어 `mariadb`기반 데이터베이스에 저장되고, 이렇게 일차적으로 저장된 값을 `airflow`가 주기적으로 읽어들여 모델을 적용해 나온 예측값을 추가합니다. 해당 과정의 로그파일은 `pyspark`로 관리되고, 이렇게 완성된 데이터베이스의 값을 다시 `streamlit`으로 읽어들여 코멘트 입력 및 통계 페이지에서 확인하게 됩니다.

데이터베이스 내 테이블은 다음과 같이 형성되어 있습니다.
- `num`: 입력된 각 데이터에 매겨지는 인덱스 번호
- `comments`: 이용자로부터 입력된 코멘트 내용
- `request_user`: 이용자가 입력한 `username`
- `request_time`: 해당 이용자의 입력 요청이 보내진 시각
- `prediction_result`: 모델을 통해 예측한 해당 코멘트의 감정. anger (분노), disgust (경멸), fear (두려움),	joy (기쁨),	neutral (중립),	sadness (슬픔),	surprise (놀람) 의 7가지로 분류됩니다.
- `prediction_score`: 모델이 자체적으로 반환한 예측 스코어 입니다. 본 어플리케이션은 특히 통계 데이터 분석에 사용됩니다.


## Usage
- `fastapi` 서버 런칭
```bash
$ uvicorn src/threekcal_model/api:app --host 0.0.0.0 --port 8000
```

- `steamlit` 서버 런칭
```bash
$ streamlit run src/threekcal_model/streamlit/main.py --server.port 9000
```
