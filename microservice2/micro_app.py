from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_microservice():
    return "hello microservice 2"