import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

question_list = ['question1', 'question2', 'question3', 'question4', 'question5'] #list of question we are going to ask
positive_list = ['yes', 'yes', 'yes', 'yes', 'yes'] #answer that will increase the final_review
negetive_list = ['no', 'no', 'no', 'no', 'no'] #answer that will decrease the final_review


round_number = 0 #to clarify what number of question we are going to ask

Final_review = 0

@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():


    round_msg = statement(question_list[round_number])

    session.attributes['question'] = positive_list[round_number]  # input the question into the session

    round_number+=1

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': str})

def answer(first, second, third):

    winning_numbers = session.attributes['question']

    if first == positive_list[round_number-1]:

        msg = render_template('win')
        Final_review += 1
    elif first == negetive_list[round_number-1]:

        msg = render_template('lose')
        Final_review -= 1

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)