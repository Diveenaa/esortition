from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, DateTimeField, FormField, FieldList
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime
from flask import flash

def validate_not_past(form, field):
    if field.data < datetime.utcnow():
        raise ValidationError("End date cannot be in the past.")

class OptionForm(FlaskForm):
    option = StringField('Option')
    # option = StringField('Option', validators=[DataRequired()])

class QuestionForm(FlaskForm):
    question_text = StringField('Question', validators=[DataRequired()])
    options = FieldList(FormField(OptionForm), min_entries=2, max_entries=6)

class ElectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired(), validate_not_past])
    voter_file = FileField('Voter File (CSV)', validators=[DataRequired()])
    question = FormField(QuestionForm)
    submit = SubmitField('Create Election')

