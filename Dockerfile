# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

CMD [ "python3", "main.py"]

EXPOSE 8000