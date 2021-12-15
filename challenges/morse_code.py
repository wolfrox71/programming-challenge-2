from flask import Blueprint, render_template

morse_code_bp = Blueprint("morse_code", __name__,
    template_folder="templates")

@morse_code_bp.route("/", methods=["POST","GET"])
def home():
    return render_template("/challenges/morse_code/home.html")