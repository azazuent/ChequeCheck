FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install python-pip python-dev

COPY ./ServerAPI.py /app
COPY ./TelegramBot.py /app
COPY ./requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ['python']

CMD ['TelegramBot.py']