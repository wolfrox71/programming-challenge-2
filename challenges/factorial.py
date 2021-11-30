from flask import Blueprint, render_template

factorial_bp = Blueprint("factorial", __name__,
    template_folder="templates")

@factorial_bp.route("/")
def home():
    return render_template("challenges/factorial/home.html")