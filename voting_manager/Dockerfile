FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /voting_manager-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FASTAPI_APP=/voting_manager-service/voting_manager_service.py

EXPOSE 5005

CMD ["uvicorn", "voting_manager_service:app", "--host=0.0.0.0", "--port=5005"]
