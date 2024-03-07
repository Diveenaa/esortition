from flask import request, jsonify
from . import db, app
from .models import Vote
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


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

@app.route('/election_results/<int:election_id>', methods=['GET'])
def get_election_results(election_id):
    # Use SQLAlchemy's group_by and func.count to aggregate votes directly in the database
    results_query = (
        db.session.query(Vote.option, func.count(Vote.option).label('vote_count'))
        .filter_by(election_id=election_id)
        .group_by(Vote.option)
        .all()
    )
    
    # Convert the aggregated results to a list of dictionaries with option_id and vote_count
    results_list = [{'option_id': option, 'vote_count': vote_count} for option, vote_count in results_query]
    
    # Return the results as JSON
    return jsonify(results_list), 200
