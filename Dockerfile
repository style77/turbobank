FROM quay.io/astronomer/astro-runtime:11.6.0

WORKDIR /app

USER root

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

