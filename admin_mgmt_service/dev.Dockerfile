FROM python

WORKDIR /admin_mgmt_service-service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# ENV FLASK_APP=/admin_mgmt_service-service/admin_service.py
