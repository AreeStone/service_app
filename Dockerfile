FROM python:3.9-alpine3.16

COPY requirements.txt /tepm/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN pip install -r /tepm/requirements.txt

RUN adduser --disabled-password service-user

USER service-user