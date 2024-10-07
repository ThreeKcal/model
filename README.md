# model
## Overview
main repository for ML service
Team Project #3 For Samdul#: Team ThreeKcal

Using `DistilRoBERTa` based text classifier model [michellejieli/emotion_text_classifier](https://huggingface.co/michellejieli/emotion_text_classifier) :
- Takes user input using `Streamlit`-based web application and performs sentiment analysis
- Takes actual sentiment labels and user comment for each input if given, for prediction feedbacck
- Airflow: check more on [this repository](https://github.com/ThreeKcal/dags/tree/main)
- Pyspark: check more on [this repository]()
<!-- add link to pyspark repo -->

![Blank_diagram_-_Page_1_2](https://github.com/user-attachments/assets/2c2cfbd5-fa7e-4cee-858b-57ccb84e6715)




## Streamlit
```bash
streamlit run src/threekcal_model/streamlit/main.py --server.port 9000
```
