# Use the official Python runtime as the base image
FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y zip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt -t /opt/python/

CMD cd /opt && zip -r9 /app/my-layer.zip .