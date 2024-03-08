FROM python

WORKDIR /voting_app-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
