from flask import Blueprint, render_template, redirect, request, url_for, flash, session
import database_mod
from info import admin_roles, get_redirect
users_bp = Blueprint("users", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

@users_bp.route("/")
def user_home():
    return render_template("/users/home.html")

@users_bp.route("/delete/",methods=["POST","GET"])
def users_delete():
    if "username" not in session:
        session["redirect"] = "users.users_delete"
        return redirect(url_for("functions.login"))
    if users_db.select_max(*session["select_args"])[0][2] not in admin_roles:
        flash("Need to be admin")
        return redirect(url_for("functions.home"))
    
    if request.method == "POST":
        users_db.remove_max(request.form["to_del"].split("¦|")[0],1,request.form["to_del"].split("¦|")[1],2)
        return redirect(url_for("functions.logout"))

    return render_template("/users/delete.html",users=users_db.read())