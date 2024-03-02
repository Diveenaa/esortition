FROM python

WORKDIR /voting_app-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=/voting_app-app/voting_app.py
ENV FLASK_ENV=development

EXPOSE 5001

CMD [ "python3", "-m" , "flask", "run", "--reload", "--port=5001", "--host=0.0.0.0"]