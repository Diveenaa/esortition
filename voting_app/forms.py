from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, validators
from wtforms.validators import DataRequired

def create_vote_form(options):
    class VoteForm(FlaskForm):
        pass

    choices = [(str(option['id']), option['text']) for option in options]
    setattr(VoteForm, 'choice', RadioField('Voting Options', choices=choices, validators=[DataRequired()]))
    setattr(VoteForm, 'submit', SubmitField('Submit Vote'))

    return VoteForm()