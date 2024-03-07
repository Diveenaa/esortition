FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /voting_manager-service/myapp

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Set environment variable to specify the main FastAPI app
# This line can be omitted if you run uvicorn with the app module and object directly in CMD
# ENV FASTAPI_APP=/voting_manager-service/voting_manager_service.py

EXPOSE 5005

# remember only use reload in development

CMD [ "python3", "-m" , "flask", "run", "--port=5005", "--host=0.0.0.0"]