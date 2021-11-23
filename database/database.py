from flask import Blueprint, render_template, redirect, request, url_for
import database_mod
database_bp = Blueprint("database", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

@database_bp.route("/")
def database_home():
    return render_template("/home.html")

@database_bp.route("/list/")
def database_list():
    return render_template("/list.html",users=users_db.read(), headings=users_db.columns())

@database_bp.route("/clear/", methods=["POST","GET"])
def database_clear():
    if request.method == "POST":
        if request.form["answer"] == "yes":
            users_db.clear()
        return redirect(url_for("functions.logout"))
    return render_template("/clear.html")