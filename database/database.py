from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from info import admin_roles
import database_mod
database_bp = Blueprint("database", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

@database_bp.route("/")
def database_home():
    return render_template("/database/home.html")

@database_bp.route("/list/")
def database_list():
    if "username" not in session or "role" not in session:
        session["redirect"] = "database.database_list"
        return redirect(url_for("functions.login"))
    if session["role"] not in admin_roles: #if the user is not an admin
        flash("Need to be admin")
        return redirect(url_for("functions.home")) #send them to the home page
    return render_template("/database/list.html",users=users_db.read(), headings=users_db.columns())

@database_bp.route("/clear/", methods=["POST","GET"])
def database_clear():
    if request.method == "POST":
        if request.form["answer"] == "yes":
            users_db.clear()
        return redirect(url_for("functions.logout"))
    return render_template("/database/clear.html")