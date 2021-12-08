from flask import Blueprint, render_template

reverse_it_bp = Blueprint("reverse_it", __name__,
    template_folder="templates")

@reverse_it_bp.route("/")
def home():
    return render_template("challenges/reverse_it/home.html")