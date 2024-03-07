from flask import request, jsonify
from . import db, app
from .models import Vote


@app.route('/votes', methods=['POST'])
def create_vote():
    data = request.get_json()
    vote = Vote(voter_id=data['voter_id'], question=data['question'],
                option=data['option'], election_id=data['election_id'])
    db.session.add(vote)
    db.session.commit()
    return jsonify(vote.id), 201 

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

