# model
## Overview
ML 어플리케이션 서비스를 위한 기본 리포지토리

팀 프로젝트 #3: 팀 ThreeKcal

`DistilRoBERTa` 기반의 text classifier 모델인 [michellejieli/emotion_text_classifier](https://huggingface.co/michellejieli/emotion_text_classifier) 을 통해:
- `Streamlit` 기반 웹 어플리케이션을 통해 사용자 입력을 받고, 해당 문장에 대한 sentiment analysis/prediction 실행 (🤬🤢😀😐😭😲)
- 해당 prediction에 대해 실제 sentiment label 및 피드백 코멘트 역시 입력
- Airflow 부분을 더 알고 싶다면 [이 리포지토리](https://github.com/ThreeKcal/dags/tree/main) 확인
- Pyspark 부분을 더 알고 싶다면 [이 리포지토리](https://github.com/ThreeKcal/pyspark/tree/main)  확인

![Blank_diagram_-_Page_1_2](https://github.com/user-attachments/assets/2c2cfbd5-fa7e-4cee-858b-57ccb84e6715)

## Usage
- `Streamlit` 어플리케이션 런칭
```bash
$ source .venv/bin/activate
$ pip install .
$ streamlit run src/threekcal_model/streamlit/main.py --server.port 9000
```

## Dev Commands
- 테스팅용 `uvicorn` 서버 런칭
```bash
$ chmod u+x run.sh
$ ./run.sh
```
