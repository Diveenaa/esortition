from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

def create_vote_form(options):
    class VoteForm(FlaskForm):
        pass

    # Dynamically add the radio fields based on options
    setattr(VoteForm, 'choice', RadioField('Voting Options', choices=[(option, option) for option in options], validators=[DataRequired()]))
    setattr(VoteForm, 'submit', SubmitField('Submit Vote'))

    return VoteForm()