from flask import Blueprint, render_template, redirect, request, url_for, session
from random import randint, choice
import datetime
import database_mod
maths_quiz_bp = Blueprint("maths_quiz", __name__,
    template_folder="templates")
maths_quiz_db = database_mod.db("main.db","maths_quiz")
maths_quiz_db.setup("username","percentage","score", "time")

@maths_quiz_bp.route("/", methods=["POST","GET"])
def maths_quiz():
    if "username" not in session:
        session["redirect"] = "challenges.maths_quiz.maths_quiz"
        return redirect(url_for("functions.home"))
    if request.method == "POST":
        score = 0
        correct = []
        for x in session["questions"]:
            if str(request.form[x]) == str(eval(x)):
                score+=1
                correct.append([x,1,request.form[x], str(eval(x))])
                continue
            correct.append([x,0,request.form[x],str(eval(x))])
        maths_quiz_db.insert(session["username"], score/len(correct)*100,  score, datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")) 
        return render_template("challenges/maths_quiz/quiz.html", questions=correct, answers="true", score=score/len(correct)*100)
    operations = ["*","-","+"]
    min_number = 0
    max_number = 10
    number_of_questions = 10
    session["questions"] = []
    for i in range(number_of_questions):
        session["questions"].append(f"{randint(min_number,max_number)}{choice(operations)}{randint(min_number,max_number)}")
    return render_template("challenges/maths_quiz/quiz.html", questions=session["questions"], answers = "false")

@maths_quiz_bp.route("/scores")
def maths_quiz_scores():
    return render_template("challenges/maths_quiz/scores.html", users=maths_quiz_db.read())