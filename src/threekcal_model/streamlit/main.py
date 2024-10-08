import streamlit as st

st.set_page_config(
    page_title="Three Kcal Team Portfolio",
    page_icon="👋",
)

st.write("# Welcome to Three kcal! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    본 어플리케이션은 text classifier 모델인 michellejieli/emotion_text_classifier 을 통한 텍스트 sentiment analysis를 진행합니다.

    - `텍스트 업로드` 페이지에서는 username과 문장을 입력받고, 이를 데이터베이스로 전송합니다! 이는 이후 Airflow를 거쳐 순차적으로 모델을 통해 7가지 감정 (🤬🤢😀😐😭😲) 중 하나의 예측값을 가지게 됩니다.

    - `코멘트 라벨적기` 페이지에서 이를 확인할 수 있습니다. 본인의 username을 선택해 분류해 보거나 데이터베이스의 전체 최신값을 확인할 수 있으며, 모델이 예측한 label이 아닌 실제 label과 그에 대한 코멘터리를 입력할 수 있습니다. 이는 다시 데이터베이스에 반영됩니다.

    - `결과 통계` 페이지에서 이를 바탕으로 만들어진 각종 통계를 살펴볼 수 있습니다. 

    기타 사항 및 본 프로그램의 코드, 동작 방식, dev 옵션 등은 본 [github README](https://github.com/ThreeKcal/model)를 참조해 주세요!
"""
)
