from flask import Blueprint, render_template, request, session, redirect, url_for
import database_mod

fruit_machine_db = database_mod.db("main.db","fruit_machine")
fruit_machine_db.setup("username","money")

fruit_machine_bp = Blueprint("fruit_machine", __name__,
    template_folder="templates")

@fruit_machine_bp.route("/", methods=["POST","GET"])
def home():
    if "username" not in session:
        session["redirect"] = "challenges.fruit_machine.home"
        return redirect(url_for("functions.login"))
    if request.method == "POST":
        fruit_machine_db.insert(session["username"], request.form["money"])
        return redirect(url_for("challenges.fruit_machine.view"))
        
    return render_template("challenges/fruit_machine/home.html")

@fruit_machine_bp.route("/view/")
def view():
    return render_template("challenges/fruit_machine/view.html", scores=fruit_machine_db.read())