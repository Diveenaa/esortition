FROM python

WORKDIR /esortition-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=/esortition-app/app.py

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--port=5000", "--host=0.0.0.0"]