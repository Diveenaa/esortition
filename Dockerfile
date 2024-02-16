FROM python

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--port=5000", "--host=0.0.0.0"]