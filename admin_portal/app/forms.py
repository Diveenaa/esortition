from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, DateTimeField, FormField, FieldList
from wtforms.validators import DataRequired

class OptionForm(FlaskForm):
    option = StringField('Option')
    # option = StringField('Option', validators=[DataRequired()])

class QuestionForm(FlaskForm):
    question_text = StringField('Question', validators=[DataRequired()])
    options = FieldList(FormField(OptionForm), min_entries=2, max_entries=6)

class ElectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    voter_file = FileField('Voter File (CSV)')
    question = FormField(QuestionForm)
    submit = SubmitField('Create Election')