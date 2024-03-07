FROM python

WORKDIR /election_mgmt_service-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .