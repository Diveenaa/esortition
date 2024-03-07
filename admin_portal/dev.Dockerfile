FROM python

WORKDIR /admin_portal-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

