FROM python

WORKDIR /election_mgmt_service-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# ENV FLASK_APP=/election_mgmt_service-service/election_service.py

EXPOSE 5003

CMD [ "python3", "-m" , "flask", "run", "--port=5003", "--host=0.0.0.0", "--reload"]