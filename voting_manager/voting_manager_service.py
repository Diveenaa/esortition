from fastapi import FastAPI

# from flask import Flask
import os


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# app = Flask(__name__)

# @app.route('/')
# def hello_microservice():
#     return "hello microservice fdsafd fdasfdasfdd safdsa 2"