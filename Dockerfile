FROM continuumio/miniconda3:4.10.3
MAINTAINER Mingxun Wang "mwang87@gmail.com"

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y build-essential

COPY . /app
WORKDIR /app

