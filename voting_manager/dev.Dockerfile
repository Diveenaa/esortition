FROM python

WORKDIR /voting_manager-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .