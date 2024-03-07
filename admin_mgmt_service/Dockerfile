FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /admin_mgmt_service-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5004

ENV FLASK_APP=/admin_mgmt_service-service/myapp/admin_service.py

CMD [ "python3", "-m" , "flask", "run", "--port=5004", "--host=0.0.0.0"]