# FROM python

# WORKDIR /voting_manager-app

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .

# ENV FLASK_APP=/voting_manager-app/voting_manager_service.py
# ENV FLASK_ENV=development

# EXPOSE 5002

# CMD [ "python3", "-m" , "flask", "run", "--port=5002", "--host=0.0.0.0", "--reload"]
FROM python

WORKDIR /voting_manager-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Set environment variable to specify the main FastAPI app
# This line can be omitted if you run uvicorn with the app module and object directly in CMD
ENV FASTAPI_APP=/voting_manager-service/voting_manager_service.py

EXPOSE 5002

# remember only use reload in development

CMD ["uvicorn", "voting_manager_service:app", "--reload", "--host=0.0.0.0", "--port=5002"]
