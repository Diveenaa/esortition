FROM python

WORKDIR /admin_app-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=/admin_app-app/app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--port=5000", "--host=0.0.0.0", "--reload"]