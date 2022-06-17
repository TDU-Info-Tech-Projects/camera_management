FROM python:3.10.4-slim-buster

COPY . /backend

WORKDIR /backend

#RUN pip install Flask
# RUN apt-get install libpq-dev
RUN pip install pipenv && pip install psycopg2-binary 

RUN pipenv install --system
