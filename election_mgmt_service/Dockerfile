FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /election_mgmt_service-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5003

CMD [ "python3", "-m" , "flask", "run", "--port=5003", "--host=0.0.0.0"]