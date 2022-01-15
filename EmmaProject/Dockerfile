# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /EmmaProject
COPY requirements.txt /EmmaProject/
RUN pip install -r requirements.txt
COPY . /EmmaProject/