from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

from flask import flash, redirect, Response
import csv
from datetime import datetime
from io import StringIO
from .models import Election, Question, Option, Voter
from .forms import ElectionForm, QuestionForm, OptionForm

from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required # only logged in user can see this
def profile():
    return render_template('profile.html', name=current_user.name)

# @main.route('/myvotes')
# @login_required # only logged in user can see this
# def myvotes():
#     return render_template('myvotes.html', name=current_user.name)

@main.route('/create_election', methods=['GET', 'POST'])
@login_required
def create_election():
    form = ElectionForm()
    while len(form.question.options) < 6:
        form.question.options.append_entry()

    if form.validate_on_submit():
        election = Election(title=form.title.data, description=form.description.data, end_date=form.end_date.data, creator=current_user)
        db.session.add(election)
        db.session.flush()
        # db.session.commit()
        
        # Handling the question and options
        question = Question(text=form.question.question_text.data, election_id=election.id)
        db.session.add(question)
        db.session.flush()
        # db.session.commit()

        for option_form in form.question.options.entries:
            if option_form.data['option']:  # Check if option text is provided
                option = Option(text=option_form.data['option'], question_id=question.id)
                db.session.add(option)
                db.session.flush()
        # db.session.commit()
        
        if form.voter_file.data:
            csv_file = form.voter_file.data.stream.read().decode("utf-8")
            csv_data = csv.reader(StringIO(csv_file), delimiter=',')
            print(csv_data)
            for row in csv_data:
                print(row)
                email = row[0]
                name = row[1] if len(row) > 1 else ''
                voter = Voter(email=email, name=name, election_id=election.id)
                db.session.add(voter)
                db.session.flush()
            # db.session.commit()
            flash('Election and voter information uploaded successfully!')
        flash('Election created successfully!')
        
        db.session.commit()


        return redirect(url_for('main.my_elections'))
    else:
        print(form.errors)
    
    return render_template('create_election.html', form=form)


@main.route('/my_elections')
@login_required
def my_elections():
    elections = Election.query.filter_by(creator_id=current_user.id).all()
    return render_template('my_elections.html', elections=elections)

@main.route('/download_voters/<int:election_id>')
@login_required
def download_voters(election_id):
    election = Election.query.get_or_404(election_id)
    if election.creator_id != current_user.id:
        return "Unauthorized", 403
    
    si = StringIO()
    cw = csv.writer(si)
    # cw.writerow(['Email', 'Name'])
    
    for voter in election.voters:
        cw.writerow([voter.email, voter.name])
    
    output = si.getvalue()
    si.close()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=voters_election.csv".format(election_id)})