FROM python

WORKDIR /microservice1-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=/microservice1-app/micro_app.py

EXPOSE 5001

CMD [ "python3", "-m" , "flask", "run", "--port=5001", "--host=0.0.0.0"]