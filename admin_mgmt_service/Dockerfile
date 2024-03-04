FROM python

WORKDIR /admin_mgmt_service-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=/admin_mgmt_service-app/admin_service.py

EXPOSE 5004

CMD [ "python3", "-m" , "flask", "run", "--port=5004", "--host=0.0.0.0"]