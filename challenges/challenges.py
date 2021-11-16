from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from random import randint, choice
import database_mod

challenges_bp = Blueprint("challenges", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

@challenges_bp.route("/")
def home():
    return render_template("challenges/home.html")

@challenges_bp.route("/maths_quiz/", methods=["POST","GET"])
def maths_quiz():
    if request.method == "POST":
        score = 0
        correct = []
        for x in session["questions"]:
            if str(request.form[x]) == str(eval(x)):
                score+=1
                correct.append([x,1,request.form[x]])
                continue
            correct.append([x,0,request.form[x]])
        return render_template("challenges/maths_quiz.html", questions=correct, answers="true", score=score/len(correct)*100)
    operations = ["*","-","+"]
    min_number = 0
    max_number = 10
    number_of_questions = 10
    session["questions"] = []
    for i in range(number_of_questions):
        session["questions"].append(f"{randint(min_number,max_number)}{choice(operations)}{randint(min_number,max_number)}")
    return render_template("challenges/maths_quiz.html", questions=session["questions"], answerws = "false")