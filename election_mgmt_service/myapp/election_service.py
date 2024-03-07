from flask import request, jsonify
from datetime import datetime
from .models import Election, Question, Option, Voter
from . import db
from . import app
import jwt
import requests
from itsdangerous import URLSafeTimedSerializer
from threading import Thread
from flask_executor import Executor


serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
executor = Executor(app)


# app = create_app()

@app.route('/')
def hello_microservice():
    return "hello"

# API gateway needed - to receive data from frontend
@app.route('/create-election', methods=['POST'])
def create_election():
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        print("no token")
        return jsonify({'error': 'Token is missing'}), 401
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    id = payload['user_id']
    # Get data
    data = request.json
    creator_id = id
    title = data.get('title')
    description = data.get('description')
    end_date_str = data.get('end_date')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    question = data.get('question')
    options = data.get('options')
    voter_file = data.get('voter_file')

    # Log the received data
    print("Received data:")
    print("creator_id:", creator_id)
    print("title:", title)
    print("description:", description)
    print("end_date:", end_date)
    print("question:", question)
    print("options:", options)
    print("voter_file:", voter_file)

    new_election = add_election_data(creator_id, title, description, end_date)
    print(new_election)
    question = add_question_data(question, new_election.id)
    add_options_data(options, question.id)
    add_voter_data(voter_file, new_election.id) # TO-DO: separate this into voter service...?
    # get_election_data()
    db.session.commit()
    # send_vote_emails_background(new_election.id)
    # send_vote_emails(new_election.id)

    voters = Voter.query.filter_by(election_id=new_election.id).all()
    election = Election.query.filter_by(id=new_election.id).first()
    end_date = election.end_date.strftime('%Y-%m-%d %H:%M:%S')

    for voter in voters:
        # Use executor to run send_vote_email function asynchronously
        executor.submit(send_vote_email, voter, new_election.id, end_date)


    # Return the received data in the response
    return jsonify({'message': 'Election created successfully'}), 200


# API gateway needed - to send data to frontend
@app.route('/fetch-elections', methods=['GET'])
def get_user_elections():
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    id = payload['user_id']
    try:
        elections = Election.query.filter_by(creator_id=id).all()
        election_data = []
        for election in elections:
            election_info = {
                'id': election.id,
                'title': election.title,
                'description': election.description,
                'created_at': election.created_at.strftime('%d-%m-%Y %H:%M'),
                'end_date': election.end_date.strftime('%d-%m-%Y %H:%M'),
                'voters': [{'email': voter.email, 'name': voter.name} for voter in election.voters]  # Extract voter emails and names
            }
            election_data.append(election_info)
        print(election_data)
        return jsonify(election_data), 200
    
    except Exception as e:
        print(f"Error retrieving user elections: {e}")
        return jsonify({'error': 'Failed to retrieve user elections'}), 500
    

# API gateway needed - to get data from frontend
@app.route('/election_voters/<election_id>', methods=['GET'])
def get_voters(election_id):
    token = request.headers.get('Authorization')
    print('here', token)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    id = payload['user_id']
    election = Election.query.get_or_404(election_id)

    if election.creator_id != int(id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    voters = []
    for voter in election.voters:
        voter_info = {'email': voter.email, 'name': voter.name}
        voters.append(voter_info)

    print(voters)
    return jsonify(voters)


def add_election_data(creator_id, title, description, end_date):
    if not all([creator_id, title, description, end_date]):
        # Data validation failed
        print("Election data valdation failed")
        return None
        
    try:
        # Create a new Election object
        new_election = Election(creator_id=creator_id,
                                title=title,
                                description=description,
                                end_date=end_date)

        # Add the new election to the database session
        db.session.add(new_election)
        
        db.session.commit()
      
        print("Election data added successfully to the database")
        return new_election
    
    except Exception as e:
        # Handle errors (e.g., database errors)
        db.session.rollback()
        print(f"Error adding election data to the database: {e}")

def add_question_data(text, election_id):
    if not all([text, election_id]):
        # Data validation failed
        print("Question data valdation failed")
        return None
        
    try:
        # Handling the question and options
        question = Question(text=text, election_id=election_id)
        db.session.add(question)
        db.session.commit()
        print("Question data added successfully to the database")
        return question

    except Exception as e:
        # Handle errors (e.g., database errors)
        db.session.rollback()
        print(f"Error adding question data to the database: {e}")

def add_options_data(options, question_id):
    if not all([options, question_id]):
        # Data validation failed
        print("Option data valdation failed")
        return None
        
    try:
        for option_text in options:
            if option_text:
                option = Option(text=option_text, question_id=question_id)
                db.session.add(option)
                db.session.commit()
        print("Option data added successfully to the database")

    except Exception as e:
        # Handle errors (e.g., database errors)
        db.session.rollback()
        print(f"Error adding option data to the database: {e}")


def add_voter_data(voter_file, election_id):
    rows = voter_file.split('\n')
    try:
        for row in rows:
            email, name = row.strip().split(',')
            voter = Voter(email=email, name=name, election_id=election_id)
            db.session.add(voter)
            db.session.commit()
        print("Voter data added successfully to the database")

    except Exception as e:
        # Handle errors (e.g., database errors)
        db.session.rollback()
        print(f"Error adding voters data to the database: {e}")


@app.route('/election-details/<int:election_id>', methods=['GET'])
def get_election_details(election_id):
    print("test")
    token = request.headers.get('Authorization')
    print(f"token is {token}")
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token is expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    # Based on election_id get the question and options.
    try:
        election = Election.query.get_or_404(election_id)
        question = Question.query.filter_by(election_id=election_id).first()
        options = Option.query.filter_by(question_id=question.id).all()

        # jsonify response
        election_details = {
            'question': question.text,
            'options': [option.text for option in options]
        }

        return jsonify(election_details), 200

    except Exception as e:
        print(f"Error retrieving election details: {e}")
        return jsonify({'error': 'Failed to retrieve election details'}), 500



# NOT IN USE - this modified version of add_voter_data will modify the function to also generate the unique token
# def add_voter_data(voter_file, election_id, end_date):
#     rows = voter_file.split('\n')
#     try:
#         for row in rows:
#             email, name = row.strip().split(',')
#             # generate token for voting
#             token_payload = {
#                 'email': email,
#                 'election_id': election_id,
#                 'exp': end_date
#             }
#             token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
#             voter = Voter(email=email, name=name, election_id=election_id, token=token)
#             db.session.add(voter)
#             db.session.commit()
#         print("Voter data added successfully to the database")

#     except Exception as e:
#         # Handle errors (e.g., database errors)
#         db.session.rollback()
#         print(f"Error adding voters data to the database: {e}")




def send_vote_emails_background(election_id):
    """
    Wrapper function to call send_vote_emails in a separate thread.
    """
    thread = Thread(target=send_vote_emails, args=(election_id,))
    thread.start()

# Calls the serverless function for each voter to send email containing unique link
def send_vote_emails(election_id):

    # get voters
    voters = Voter.query.filter_by(election_id=election_id).all()
    election = Election.query.filter_by(id=election_id).first()
    end_date = election.end_date.strftime('%Y-%m-%d %H:%M:%S')
    
    email_service_url = "https://esortition-email-send.azurewebsites.net/api/HttpTrigger2?code=iSYkxWBvsPD9hLrtAB9aMW-r9pbazdvg0sh1ow8SJb8AAzFu5bTkcA=="

    for voter in voters:
        print(f"sending email to: {voter.email}")
        token = serializer.dumps({'voter_id': voter.id, 'election_id': election_id}, salt='vote-token')
        voting_link = f"http://localhost:5002/vote?token={token}"
        # HTML email body
        email_body_html = f"""
        <html>
        <body>
            <p>Hello {voter.name},</p>
            
            <p>Please use the following link to cast your vote in the election:</p>
            <a href="{voting_link}">{voting_link}</a>
            
            <p>This link will expire at the end of the election period on <strong>{end_date}</strong>.</p>
            
            <p>Thank you for participating!</p>
        </body>
        </html>
        """

        # Plain text email body
        email_body_plain = f"""
        Hello {voter.name},
        
        Please use the following link to cast your vote in the election:
        {voting_link}
        
        This link will expire at the end of the election period on {end_date}.
        
        Thank you for participating!
        """

        # payload for serverless function
        payload = {
            "recipient_address": voter.email,
            "subject": "Your Voting Link for the Upcoming Election",
            "plain_text_body": email_body_html,
            "html_body": email_body_html
        }

        # API call to the serverless email sending function
        try:
            requests.post(email_service_url, json=payload)
            # response = requests.post(email_service_url, json=payload)
            # if response.status_code == 200:
            #     print(f"Email successfully sent to {voter.email}")
            # else:
            #     print(f"Failed to send email to {voter.email}. Response Code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while sending email to {voter.email}: {e}")



def send_vote_email(voter, election_id, end_date):
    # Generate the token and voting link
    token = serializer.dumps({'voter_id': voter.id, 'election_id': election_id}, salt='vote-token')
    voting_link = f"http://localhost:5002/vote?token={token}"
    
    email_service_url = "https://esortition-email-send.azurewebsites.net/api/HttpTrigger2?code=iSYkxWBvsPD9hLrtAB9aMW-r9pbazdvg0sh1ow8SJb8AAzFu5bTkcA=="

    # HTML email body
    email_body_html = f"""
    <html>
    <body>
        <p>Hello {voter.name},</p>
        
        <p>Please use the following link to cast your vote in the election:</p>
        <a href="{voting_link}">{voting_link}</a>
        
        <p>This link will expire at the end of the election period on <strong>{end_date}</strong>.</p>
        
        <p>Thank you for participating!</p>
    </body>
    </html>
    """

    # Note: Your original function sets 'plain_text_body' with the HTML content.
    # Adjust if you meant to use a different plain text content.
    email_body_plain = f"""
    Hello {voter.name},
    
    Please use the following link to cast your vote in the election:
    {voting_link}
    
    This link will expire at the end of the election period on {end_date}.
    
    Thank you for participating!
    """

    # Construct the payload with both HTML and plain text versions of the email
    payload = {
        "recipient_address": voter.email,
        "subject": "Your Voting Link for the Upcoming Election",
        "plain_text_body": email_body_plain,
        "html_body": email_body_html
    }

    # Use the current application context to access app-level configurations or objects
    try:
        # Sending the email without waiting for a response
        requests.post(email_service_url, json=payload)  # short connection and read timeout
        print(f"Email queued to be sent to: {voter.email}")
    except Exception as e:
        print(f"An error occurred while attempting to queue email to {voter.email}: {e}")