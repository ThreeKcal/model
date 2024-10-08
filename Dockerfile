FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y vim

COPY src/threekcal_model/api.py /code/
COPY run.sh /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/ThreeKcal/model.git@0.4.0/streamlit

CMD ["sh", "run.sh"]
