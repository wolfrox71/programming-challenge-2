from flask import Blueprint, render_template, redirect, request, url_for, flash, session
import database_mod

challenges_bp = Blueprint("challenges", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

@challenges_bp.route("/")
def home():
    return render_template("challenges/home.html")

@challenges_bp.route("/maths_quiz")
def maths_quiz():
    return render_template("challenges/maths_quiz.html")