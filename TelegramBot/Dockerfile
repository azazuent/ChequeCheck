FROM python:latest

COPY ./ServerAPI.py /app/
COPY ./TelegramBot.py /app/
COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["TelegramBot.py"]
