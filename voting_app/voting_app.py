from flask import Flask, request, render_template
import requests


app = Flask(__name__)

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

API_GATEWAY_URL = "http://nginx-api-gateway/voting/"

@app.route('/', methods=['GET', 'POST'])
def vote():
    # if request.method == 'POST':
    #     vote = request.form['vote']
        # Here, instead of incrementing a local dict, you'd call the microservice
        # to register the vote. This example just fetches data.
        
    # Fetch voter information from the voting_manager microservice
    response = requests.get(API_GATEWAY_URL + "votes/")
    if response.status_code == 200:
        voters = response.json()  # Assuming the response is JSON containing voter data
    else:
        voters = []  # Handle errors or empty responses as needed

    return render_template('voting.html', voters=voters)


