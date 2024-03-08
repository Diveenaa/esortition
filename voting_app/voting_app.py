from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from datetime import datetime
import requests
import os
from forms import create_vote_form
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
VOTE_MANAGER_API = API_GATEWAY_URL + "voting/"
ELECTION_MGMT_API_GATEWAY_URL = API_GATEWAY_URL + "election_mgmt_service/"

# def vote():

#     if request.method == 'POST':
#         # Extract vote details from the form submission
#         vote_data = {
#             "username": request.form.get("username"),  # Example field
#             "age": int(request.form.get("age")),  # Example field
#             # Add additional fields as needed based on your voting form and Vote model
#         }
        
#         # Submit the vote to the microservice via the API gateway
#         response = requests.post(VOTE_MANAGER_API + "votes/", json=vote_data)
#         if response.status_code == 201:  # Assuming 201 Created response on successful vote submission
#             # Redirect to a success page or back to voting page with a success message
#             return redirect(url_for('vote_success'))
#         else:
#             # Handle errors or unsuccessful vote submission
#             # This could involve rendering the voting page with an error message
#             error_message = "Failed to submit vote. Please try again."
#             return render_template('voting.html', error_message=error_message)
        
#     # Fetch voter information from the voting_manager microservice
#     response = requests.get(VOTE_MANAGER_API + "votes/")
#     if response.status_code == 200:
#         voters = response.json()  # Assuming the response is JSON containing voter data
#     else:
#         voters = []  # Handle errors or empty responses as needed

#     return render_template('voting.html', voters=voters)


# @app.route('/success', methods=['GET'])
# def vote_success():
#     return render_template('vote_success.html')



@app.route('/vote', methods=['GET', 'POST'])
def vote():
    
    token = request.args.get('token', None)

    if not token:
        return jsonify({'error': 'Missing voting token'}), 400
    
    # Decode the token to get the voter_id and election_id
    try:
        token_data = serializer.loads(token, salt='vote-token')
        voter_id = token_data['voter_id']
        election_id = token_data['election_id']
    except Exception as e:
        return jsonify({'error': 'Invalid or expired token'}), 400


    # token = session.get('token')
    # Correctly construct the URL to include the full path to the election-details endpoint
    microservice_url = f'{ELECTION_MGMT_API_GATEWAY_URL}election-details/{election_id}'

    # headers = {'Authorization': f'Bearer {token}'}
    # response = requests.get(microservice_url, headers=headers)
    # response = make_request(microservice_url, token)
    response = make_request(microservice_url)

    if response.status_code == 200:
        election_details = response.json()
        question = election_details['question']
        options = election_details['options']

        end_date_str = election_details['end_date']
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
        # Compare with current datetime
        if datetime.now() > end_date:
            # Election has ended, voting is not allowed
            return render_template('vote_outcome.html', outcome='election_ended', end_date=end_date_str)

        VoteForm = create_vote_form(options)
        form = VoteForm

        if form.validate_on_submit():
            selected_option = request.form['choice']
            
            # voter_id = election_details.get('voter_id')
            question_id = election_details['question']['id']
            selected_option_id = selected_option
            # election_id = election_details.get('election_id')

            vote_data = {
                'voter_id': voter_id,
                'question': question_id,
                'option': selected_option_id,
                'election_id': election_id
            }
            print(f"Vote Data: {vote_data}")
            
            # vote_response = requests.post(f'{VOTE_MANAGER_API}/votes', json=vote_data, headers={'Authorization': f'Bearer {token}'})
            vote_response = requests.post(f'{VOTE_MANAGER_API}/votes', json=vote_data)
            
            if vote_response.status_code == 201:
                return render_template('vote_outcome.html', outcome='success')
            elif vote_response.status_code == 409:
                return render_template('vote_outcome.html', outcome='already_voted')
            else:
                # Handle other errors
                return render_template('vote_outcome.html', outcome='error', error_message=vote_response.json().get('error'))

        return render_template('vote_form.html', form=form, question=question['text'], election_id=election_id)
    else:
        # Handle errors
        return jsonify({'error': 'Failed to load election details'}), response.status_code
    

def make_request(url, token=None):
    headers = {
        'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
        'Access-Control-Allow-Headers': 'Content-Type',  # Specify allowed headers
    }
    if token:
        headers['Authorization'] = token  # Include the token in the Authorization header

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response
    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None