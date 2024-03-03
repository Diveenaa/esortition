from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, select, create_engine
from typing import List
# from flask import Flask
import os

class Vote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    age: int
    # item_id: str  # Identifier for the item being voted on
    # timestamp: datetime = Field(default_factory=datetime.utcnow)

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/votes/", response_model=Vote)
def create_vote(vote: Vote, session: Session = Depends(get_session)):
    session.add(vote)
    session.commit()
    session.refresh(vote)
    return vote

@app.get("/votes/", response_model=List[Vote])
def read_votes(session: Session = Depends(get_session)):
    result = session.exec(select(Vote)).all()
    return result


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# app = Flask(__name__)

# @app.route('/')
# def hello_microservice():
#     return "hello microservice fdsafd fdasfdasfdd safdsa 2"


# from flask import Flask, request, render_template
# from flask_sqlalchemy import SQLAlchemy
# import os


# app = Flask(__name__)
# # Configure the SQLALCHEMY_DATABASE_URI for your app before initializing the SQLAlchemy instance
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") 

# # Initialize the SQLAlchemy instance
# # db = SQLAlchemy(app)

# # Define the Vote model
# # class Vote(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(80), unique=False, nullable=False)
# #     age = db.Column(db.Integer)
# #     vote = db.Column(db.String(80), unique=False, nullable=False)

# votes = {'yes': 0, 'no': 0}
# @app.route('/', methods=['GET', 'POST'])
# def vote():
#     if request.method == 'POST':
#         vote = request.form['vote']
#         if vote == 'yes':
#             votes['yes'] += 1
#         elif vote == 'no':
#             votes['no'] += 1
#     return render_template('voting.html')

# # with app.app_context():
# #     db.create_all()