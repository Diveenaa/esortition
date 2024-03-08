FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /voting_manager-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5005

ENV FLASK_APP=/voting_manager-service/myapp:app

CMD [ "python3", "-m" , "flask", "run", "--port=5005", "--host=0.0.0.0"]