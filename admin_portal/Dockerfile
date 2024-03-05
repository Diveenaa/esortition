FROM python

WORKDIR /admin_portal-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# ENV FLASK_APP=/admin_portal-app/app.py
ENV FLASK_ENV=development

EXPOSE 5001

CMD [ "python3", "-m" , "flask", "run", "--port=5001", "--host=0.0.0.0", "--reload"]