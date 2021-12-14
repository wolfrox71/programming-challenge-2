from flask import Blueprint, render_template, redirect, request, url_for, flash, session
import database_mod
from info import allow_blank_passwords, hash, get_redirect

functions_bp = Blueprint("functions", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")
@functions_bp.route("/")
@functions_bp.route("/home/")
def home():
    if "username" in session:
        session["select_args"] = [session["username"], 1, session["password"],2]
        if "role" not in session:
            session["role"] = users_db.select_max(*session["select_args"])[0][2]
    
        return render_template("menu/home.html")
    return redirect(url_for("functions.login"))

@functions_bp.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("functions.home"))



@functions_bp.route("/login/",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username.strip()) == 0 or len(password.strip()) == 0 and not allow_blank_passwords:
            flash("Do not leave usernames or passwords blank","warning")
            return render_template("/menu/login.html")
        session["username"] = username
        session["password"] = hash(password)
        if "select_args" not in session:
            session["select_args"] = [session["username"], 1, session["password"],2]

        if len(users_db.select_max(*session["select_args"])):
            session["logged in"] = True
            flash(f"logged in as user {username}", "info")
            if "role" not in session:
                session["role"] = users_db.select_max(*session["select_args"])[0][2]

            responce = get_redirect()
            if responce is not None:
                return redirect(responce)
            return redirect(url_for("functions.home"))
        return redirect(url_for("user.user_create"))

    return render_template("/menu/login.html")