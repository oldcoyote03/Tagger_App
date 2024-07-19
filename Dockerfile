# syntax=docker/dockerfile:1.0
FROM python:3.12-slim-bookworm
RUN apt-get -y update
RUN apt-get -y upgrade
RUN python -m pip install --upgrade pip
RUN mkdir /app
WORKDIR /app
COPY . .
# ENV LOG_FILE=/var/log/app.log

RUN pip install -r requirements.txt
CMD [ "sleep", "infinity" ]
# CMD [ "python", "./run.py"]