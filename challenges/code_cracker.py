from flask import Blueprint, render_template, request, session, redirect, url_for

code_cracker_bp = Blueprint("code_cracker", __name__,
    template_folder="templates")

@code_cracker_bp.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        number=""
        for i in range(1,5):
            number += str(request.form[f"num{i}"])
        session["code_cracker_number"] = number
        return redirect(url_for("challenges.code_cracker.cracker"))
    return render_template("challenges/code_cracker/home.html")

@code_cracker_bp.route("/cracker/")
def cracker():
    if "code_cracker_number" not in session:
        return redirect(url_for("challenges.code_cracker.home"))
    return render_template("/challenges/code_cracker/cracker.html", number=session["code_cracker_number"])