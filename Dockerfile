FROM python:3.11-alpine

RUN pip install airflow-helper==0.2.0
WORKDIR /app

ENTRYPOINT [ "airflow-helper" ]
