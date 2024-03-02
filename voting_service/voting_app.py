from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
# Configure the SQLALCHEMY_DATABASE_URI for your app before initializing the SQLAlchemy instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") 

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Define the Vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer)
    vote = db.Column(db.String(80), unique=False, nullable=False)

votes = {'yes': 0, 'no': 0}
@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote = request.form['vote']
        if vote == 'yes':
            votes['yes'] += 1
        elif vote == 'no':
            votes['no'] += 1
    return render_template('voting.html')

with app.app_context():
    db.create_all()




