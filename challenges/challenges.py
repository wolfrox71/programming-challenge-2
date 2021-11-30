from flask import Blueprint, render_template
import database_mod
from challenges.maths_quiz import maths_quiz_bp
from challenges.factorial import factorial_bp

challenges_bp = Blueprint("challenges", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

challenges_bp.register_blueprint(maths_quiz_bp, url_prefix="/maths_quiz/")
challenges_bp.register_blueprint(factorial_bp, url_prefix="/factorial/")

@challenges_bp.route("/")
def home():
    return render_template("challenges/home.html")
