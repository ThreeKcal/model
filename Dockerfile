FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y vim

COPY src/threekcal_model/api.py /code/
COPY run.sh /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/ThreeKcal/model.git@sun/0.2.0

CMD ["sh", "run.sh"]
