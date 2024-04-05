FROM pytorch/pytorch:latest

RUN apt-get update -y
RUN apt-get install -y libgl1-mesa-glx zbar-tools libpq-dev

COPY ./ChequeAPI.py /app/
COPY ./DatabaseAPI.py /app/
COPY ./Server.py /app/
COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ['python']

CMD ['Server.py']