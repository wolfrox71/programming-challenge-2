from flask import Blueprint, render_template
import database_mod
from challenges.maths_quiz import maths_quiz_bp
from challenges.factorial import factorial_bp
from challenges.code_cracker import code_cracker_bp
from challenges.caesar_cipher import caesar_cipher_bp
from challenges.reverse_it import reverse_it_bp
from challenges.fruit_machine import fruit_machine_bp
from challenges.pangram import pangram_bp
from challenges.notes import notes_bp
from challenges.morse_code import morse_code_bp

challenges_bp = Blueprint("challenges", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

challenges_bp.register_blueprint(maths_quiz_bp, url_prefix="/maths_quiz/")
challenges_bp.register_blueprint(factorial_bp, url_prefix="/factorial/")
challenges_bp.register_blueprint(code_cracker_bp, url_prefix="/code_cracker/")
challenges_bp.register_blueprint(caesar_cipher_bp, url_prefix="/caesar_cipher/")
challenges_bp.register_blueprint(reverse_it_bp, url_prefix="/reverse_it/")
challenges_bp.register_blueprint(fruit_machine_bp, url_prefix="/fruit_machine/")
challenges_bp.register_blueprint(pangram_bp, url_prefix="/pangram/")
challenges_bp.register_blueprint(notes_bp, url_prefix="/notes/")
challenges_bp.register_blueprint(morse_code_bp, url_prefix="/morse_code/")

@challenges_bp.route("/")
def home():
    return render_template("challenges/home.html")
