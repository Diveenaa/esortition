from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, DateTimeField
from wtforms.validators import DataRequired

class ElectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    voter_file = FileField('Voter File (CSV)')
    submit = SubmitField('Create Election')