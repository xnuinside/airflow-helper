FROM python:3.11-alpine

RUN pip install airflow-helper==0.1.2
WORKDIR /app

ENTRYPOINT [ "airflow-helper" ]
