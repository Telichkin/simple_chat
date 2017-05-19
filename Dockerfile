FROM python:3.6

RUN apt-get update -y \
  && apt-get install python-gevent-websocket -y

ADD . /chat
WORKDIR /chat
RUN pip install -r requirements.txt