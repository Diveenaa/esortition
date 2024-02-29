FROM python

WORKDIR /microservice-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=/microservice-app/micro_app.py
ENV FLASK_ENV=development

EXPOSE 5002

CMD [ "python3", "-m" , "flask", "run", "--port=5002", "--host=0.0.0.0", "--reload"]