FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /vclite

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN apk update && apk add gcc python3-dev libffi-dev libc-dev
RUN python3 -m pip install -r requirements.txt
