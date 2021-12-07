from flask import Blueprint, render_template

caesar_cipher_bp = Blueprint("caesar_cipher", __name__,
    template_folder="templates")

@caesar_cipher_bp.route("/")
def home():
    return render_template("challenges/caesar_cipher/home.html")