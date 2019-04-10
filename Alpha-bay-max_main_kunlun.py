import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

total_question = 5 # total number of the question
question_list = ['Do you feel bad today',\
                 'Do you have any intimate relation in this week',\
                 'Did you exercise in the last three days',\
                 'Do you talk to more than two friends in last two days',\
                  'Are you facing any deadline right now'] #list of question we are going to ask
positive_list = ['yes', 'yes', 'yes', 'yes', 'yes'] #answer that will increase the final_review
negative_list = ['no', 'no', 'no', 'no', 'no'] #answer that will decrease the final_review
positive_points = [1, 2, 3, 4, 5]
negative_points = [-1, -2, -3, -4, -5]
mood_state = ['fine', 'sad', 'very sad', 'desperate']
suggestions = ['We think more exercise, have more connects with your friends would help']


round_number = 0 #to clarify what number of question we are going to ask

Final_review = 0

@ask.launch

def new_game():


    welcome_msg = 'Welcome, this is alpha bay max, we are going to help you analyze your current mood state,\
                    and try our best to make you feel better'

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():


    round_msg = question_list[round_number]

    session.attributes['positive_ans'] = positive_list[round_number]  # input the question into the session

    round_number+=1

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': str})

def answer(first, second, third):

    winning_numbers = session.attributes['positive_ans']
    if round_number < total_question:
        msg = 'Thanks for your answer, we are going to ask you another question'
    else:
        msg = "Thanks, we have ask all our questions, and we'll start to analyze"

    if first == positive_list[round_number-1]:
        Final_review += positive_points[round_number-1]
    elif first == negetive_list[round_number-1]:
        Final_review += negative_points[round_number-1]

    mood_state_ana = classify_func(Final_review)

    if round_number == total_question:
        msg += 'we think now you are {}'.format(str(mood_state_ana))
        msg += suggestions[0]
    return statement(msg)

def classify_func(review_score):
    if (review_score > 0):
        return mood_state[0]
    if (review_score < -13):
        return mood_state[3]
    if (review_score < -8):
        return mood_state[2]
    if (review_score <= 0):
        return mood_state[1]


if __name__ == '__main__':

    app.run(debug=True)