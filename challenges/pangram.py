from flask import Blueprint, render_template

pangram_bp = Blueprint("pangram", __name__,
    template_folder="templates")

@pangram_bp.route("/")
def home():
    return render_template("challenges/pangram/home.html")