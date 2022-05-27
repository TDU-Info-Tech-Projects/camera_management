FROM python:3.10.4-slim-buster

COPY . /backend

WORKDIR /backend

#RUN pip install Flask
RUN pip install pipenv

RUN pipenv install --system
