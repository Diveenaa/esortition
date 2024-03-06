from flask import Flask, request, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)


API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
VOTE_MANAGER_API = API_GATEWAY_URL + "voting/"

@app.route('/', methods=['GET', 'POST'])
def vote():

    if request.method == 'POST':
        # Extract vote details from the form submission
        vote_data = {
            "username": request.form.get("username"),  # Example field
            "age": int(request.form.get("age")),  # Example field
            # Add additional fields as needed based on your voting form and Vote model
        }
        
        # Submit the vote to the microservice via the API gateway
        response = requests.post(VOTE_MANAGER_API + "votes/", json=vote_data)
        if response.status_code == 201:  # Assuming 201 Created response on successful vote submission
            # Redirect to a success page or back to voting page with a success message
            return redirect(url_for('vote_success'))
        else:
            # Handle errors or unsuccessful vote submission
            # This could involve rendering the voting page with an error message
            error_message = "Failed to submit vote. Please try again."
            return render_template('voting.html', error_message=error_message)
        
    # Fetch voter information from the voting_manager microservice
    response = requests.get(VOTE_MANAGER_API + "votes/")
    if response.status_code == 200:
        voters = response.json()  # Assuming the response is JSON containing voter data
    else:
        voters = []  # Handle errors or empty responses as needed

    return render_template('voting.html', voters=voters)


@app.route('/success', methods=['GET'])
def vote_success():
    return render_template('vote_success.html')
