from flask import request, jsonify
from . import db, app
from .models import Vote


@app.route('/votes', methods=['POST'])
def create_vote():
    vote_data = request.json  # Get data from request body
    vote = Vote(**vote_data)  # Create a Vote instance with the provided data
    db.session.add(vote)  # Add the new vote to the session
    db.session.commit()  # Commit the session to save changes to the database
    return jsonify({'message': 'vote created successfully'}), 200  # Return the created vote as JSON with a 201 status code

@app.route('/votes', methods=['GET'])
def read_votes():
    try:
        votes_query = Vote.query.all()  # Attempt to query all votes from the database
        votes = [vote.as_dict() for vote in votes_query]  # Attempt to convert vote objects to dictionaries
        return jsonify(votes)  # Return the votes as JSON
    except Exception as e:
        # Log the exception if you have logging set up, e.g., app.logger.error(f"Error reading votes: {str(e)}")
        
        # Return a JSON error response with a 500 Internal Server Error status code
        return jsonify({"error": "An error occurred while fetching votes."}), 500

