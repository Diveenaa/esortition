from fastapi import FastAPI, Depends, status
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


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()
# 
#   REMOVING ABOVE AND RELYING ON ALEMBIC COMMAND 


@app.post("/votes/", status_code=status.HTTP_201_CREATED, response_model=Vote)
def create_vote(vote: Vote, session: Session = Depends(get_session)):
    session.add(vote)
    session.commit()
    session.refresh(vote)
    return vote

@app.get("/votes/", response_model=List[Vote])
def read_votes(session: Session = Depends(get_session)):
    result = session.exec(select(Vote)).all()
    return result
