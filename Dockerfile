FROM quay.io/astronomer/astro-runtime:11.6.0

WORKDIR /app

USER root

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && pip install --no-cache-dir dbt-postgres && deactivate

USER astro

ENV POSTGRES_CONNECTOR=postgres://postgres:postgres@127.0.0.1:5432/public
ENV POSTGRES_CONN_ID=postgres://postgres:postgres@127.0.0.1:5432/turbobank
ENV DBT_PROJECT_DIR=/usr/local/airflow/dbt/turbobank
ENV DBT_DOCS_PATH=/usr/local/airflow/dbt-docs
