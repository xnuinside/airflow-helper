FROM python:3.11-alpine

RUN pip install airflow-helper
WORKDIR /app

ENTRYPOINT [ "airflow-helper" ]
