import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch

def new_game():
    
    welcome_msg = 'Welcome, this is alpha bay max, we are going to help you analyze your current mood state,\
                    and try our best to make you feel better'

    session.attributes['total_question'] = 5
    #sample questions
    session.attributes['question_list'] = ['Do you feel bad today',\
                     'Did you exercise in the last three days',\
                     'Do you talk to more than two friends in last two days',\
                      'Are you facing any deadline right now',\
                      'Did you feel stressful over 5 times a week',\
                       'Do you drink a lot or use drugs'] #list of question we are going to ask
    
    session.attributes['positive_answer'] = ['yes', 'no', 'no', 'no', 'yes']

    session.attributes['positive_points'] = [1, 2, 3, 4, 5, 6]

    session.attributes['negative_points'] = [-1, -2, -3, -4, -5, 6]

    session.attributes['mood_state'] = ['fine', 'sad', 'very sad', 'desperate']
    
    session.attributes['suggestions'] = 'We think more exercise, have more connects with your friends would help'

    session.attributes['round_number'] = 0

    session.attributes['Final_review'] = 0

    return question(welcome_msg)

@ask.intent("YesIntent")

def next_round1():
    round_number = session.attributes['round_number']

    round_msg = session.attributes['question_list'][round_number]

    return question(round_msg)

@ask.intent("AnswerIntent", convert={'first': str})

def answer1(first):
    round_number = session.attributes['round_number']
    total_question = session.attributes['total_question']

    if first == session.attributes['positive_answer'][round_number]:
        session.attributes['Final_review'] += session.attributes['positive_points'][round_number]
    else:
        session.attributes['Final_review'] += session.attributes['negative_points'][round_number]

    if round_number < total_question - 1:
        #msg = 'Thanks for your answer, we are going to ask you another question'
        session.attributes['round_number'] += 1

        next_round()
    else:
        msg = "Thanks, we have ask all our questions, and we'll start to analyze"

        final_score = session.attributes['Final_review']
        mood_state_ana = classify_func(final_score)

        msg = 'we think now you are {}'.format(str(mood_state_ana))
        msg += session.attributes['suggestions']
        return question(msg)

def classify_func(review_score):
    if (review_score > 0):
        return session.attributes['mood_state'][0]
    if (review_score < -13):
        return session.attributes['mood_state'][3]
    if (review_score < -8):
        return session.attributes['mood_state'][2]
    if (review_score <= 0):
        return session.attributes['mood_state'][1]

if __name__ == '__main__':

    app.run(debug=True)
