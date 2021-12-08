from flask import Blueprint, render_template

fruit_machine_bp = Blueprint("fruit_machine", __name__,
    template_folder="templates")

@fruit_machine_bp.route("/")
def home():
    return render_template("challenges/fruit_machine/home.html")