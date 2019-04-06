import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

question_list = ['question1', 'question2', 'question3', 'question4', 'question5'] #list of question we are going to ask

round_number = 0 #to clarify what number of question we are going to ask

Final_review = 0

@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():


    round_msg = render_template('round', numbers=numbers)

    session.attributes['question'] = question_list[round_number]  # input the question into the session

    round_number+=1

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': str})

def answer(first, second, third):

    winning_numbers = session.attributes['question']

    if first == 'yes':

        msg = render_template('win')
        Final_review += 1
    elif first == 'no':

        msg = render_template('lose')
        Final_review -= 1
        
    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)