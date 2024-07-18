# syntax=docker/dockerfile:1.0
FROM python:3.12-slim-bookworm
# FROM python:3.8.12-slim-buster
RUN apt-get -y update
RUN apt-get -y upgrade
RUN python -m pip install --upgrade pip
RUN mkdir /app
WORKDIR /app
COPY . .
# COPY test test
# COPY run.py run.py
# COPY settings.py settings.py
# COPY manage_db.py manage_db.py
# COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
CMD [ "sleep", "infinity" ]
# CMD [ "python", "./run.py"]