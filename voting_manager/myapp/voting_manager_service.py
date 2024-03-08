from flask import request, jsonify
from . import db, app
from .models import Vote


@app.route('/votes', methods=['POST'])
def create_vote():
    data = request.get_json()
    voter_id = data['voter_id']
    question_id = data['question']
    election_id = data['election_id']

    # check if voter has already voted
    existing_vote = Vote.query.filter_by(voter_id=voter_id, question=question_id, election_id=election_id).first()
    if existing_vote:
        return jsonify({'message': 'You have already voted for this question.'}), 409

    new_vote = Vote(voter_id=voter_id, question=question_id,
                    option=data['option'], election_id=election_id)
    db.session.add(new_vote)
    db.session.commit()
    return jsonify(new_vote.id), 201

@app.route('/voters', methods=['GET'])
def read_votes():
    try:
        votes_query = Vote.query.all()  # Attempt to query all votes from the database
        votes = [vote.as_dict() for vote in votes_query]  # Attempt to convert vote objects to dictionaries
        return jsonify(votes)  # Return the votes as JSON
    except Exception as e:
        # Log the exception if you have logging set up, e.g., app.logger.error(f"Error reading votes: {str(e)}")
        
        # Return a JSON error response with a 500 Internal Server Error status code
        return jsonify({"error": "An error occurred while fetching votes."}), 500

