FROM python

WORKDIR /voting_manager-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=/voting_manager-app/voting_manager_service.py
ENV FLASK_ENV=development

EXPOSE 5002

CMD [ "python3", "-m" , "flask", "run", "--port=5002", "--host=0.0.0.0", "--reload"]