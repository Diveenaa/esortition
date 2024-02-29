from flask import Flask, request, render_template


app = Flask(__name__)

votes = {'yes': 0, 'no': 0}
@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote = request.form['vote']
        if vote == 'yes':
            votes['yes'] += 1
        elif vote == 'no':
            votes['no'] += 1
    return render_template('voting.html')





