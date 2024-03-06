from . import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer)
    question = db.Column(db.Integer)
    option = db.Column(db.Integer)
    election_id = db.Column(db.Integer)

    def as_dict(self):
        """Convert instance to dictionary."""
        return {
            "id": self.id,
            "voter_id": self.voter_id,
            "question": self.question,
            "option": self.option,
            "election_id": self.election_id
        }