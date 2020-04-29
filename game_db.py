import pgzrun
import random
from pgzero.rect import Rect
from dbmanager import DBManager
from models import Question

db = DBManager('questions.db')

WIDTH = 800
HEIGHT = 600

question_box = Rect(20, 20, 600, 200)
timer_box = Rect(640, 20, 140, 200)
answer_box1 = Rect(20, 254, 370, 150)
answer_box2 = Rect(410, 254, 370, 150)
answer_box3 = Rect(20, 430, 370, 150)
answer_box4 = Rect(410, 430, 370, 150)

answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]

score = 0
time_left = 10  # number of seconds the player has to answer each question


scores = 0
#questions = [q1, q2, q3]
questions = db.select_questions()

def draw():
    screen.fill("#eeeeee")
    screen.draw.filled_rect(question_box, "#7B8E95")
    screen.draw.filled_rect(timer_box, "#43AFA0")

    for box in answer_boxes:
        screen.draw.filled_rect(box, "#7F9BB3")

    screen.draw.textbox(str(time_left), timer_box, color=("white"))
    screen.draw.textbox(question.text, question_box, color=("white"))

    index = 0
    for box in answer_boxes:
        screen.draw.textbox(str(question.answers[index]), box)
        index = index + 1

def game_over():
    global question
    message = f'Опрос завершен. Правильных ответов: {scores}'
    question = Question(
        text=message,
        answers=['-', '-', '-', '-'],
        correct_answer=''
    )
    clock.unschedule(update_timer)

def get_next_question():
    global question, time_left
    if len(questions) > 0:
        time_left = 10
        question = questions.pop()
    else:
        game_over()

def on_mouse_down(pos):
    global question, scores
    index = 0
    for box in answer_boxes:
        if box.collidepoint(pos):
            user_answer = question.answers[index]
            if user_answer == question.correct_answer:
                scores += 1
            get_next_question()

        index += 1

def update_timer():
    global time_left
    if time_left <= 0:
        get_next_question()
    else:
        time_left -= 1


if questions:
    question = questions.pop()
else:
    game_over()

clock.schedule_interval(update_timer, 1)
pgzrun.go()