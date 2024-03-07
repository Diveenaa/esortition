FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /admin_portal-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5001

CMD [ "python3", "-m" , "flask", "run", "--port=5001", "--host=0.0.0.0"]