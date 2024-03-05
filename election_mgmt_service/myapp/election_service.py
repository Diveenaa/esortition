from flask import Flask, request, jsonify
from datetime import datetime
from .models import Election, Question, Option, Voter
from . import db
from . import app
import jwt

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

    # Return the received data in the response
    return jsonify({'message': 'Election created successfully'}), 200


# API gateway needed - to send data to frontend
@app.route('/fetch-elections/', methods=['GET'])
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