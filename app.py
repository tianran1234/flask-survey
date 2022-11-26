from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def show_survey():
    return render_template('show_survey.html', survey=survey)

 
@app.route('/begin', methods=["POST"])
def start_survey():

    session['responses'] = []

    return redirect('/questions/0')


@app.route('/questions/<int:num>')
def show_question(num):
    responses = session.get('responses')

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you')

    if (len(responses) != num):
        flash(f"Invalid question number: {num}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[num]

    return render_template(
        'question.html', question_num=num, question=question,survey=survey)


@app.route('/answer',methods=["POST"])
def handle_response():
    response = request.form['answer']

    responses = session['responses']
    responses.append(response)
    session['responses'] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you')

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/thank_you')
def complete():
    return render_template('thank_you.html')
   
