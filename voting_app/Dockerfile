FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /voting_app-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5002

ENV FLASK_APP=/voting_app-app/voting_app.py
ENV FLASK_ENV='production'

CMD [ "python3", "-m" , "flask", "run", "--port=5002", "--host=0.0.0.0"]