from flask import Blueprint, render_template, redirect, request, url_for, flash, session
import database_mod
from info import roles, defualt_role, get_redirect
user_bp = Blueprint("user", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

@user_bp.route("/")
def user_home():
    return render_template("/user/home.html")

@user_bp.route("/create/", methods=["POST","GET"])
def user_create():
    if "username" not in session: #if the user hasnt tried to login
        session["redirect"] = "user.user_create"
        return redirect(url_for("functions.login")) # get the users username and password
    if "select_args" not in session:
        session["select_args"] = [session["username"], 1, session["password"],2]
        
    if len(users_db.select_max(*session["select_args"])) != 0: #see if the user account already exists
        flash("You are already logged in. Sign out and login to create a new account")
        return redirect(url_for("functions.home")) # return to the home page to be redirected
    
    if request.method == "POST":
        if request.form["create_user"] == "yes": #make sure the user wants to create the user
            users_db.insert(session["username"], session["password"], defualt_role) #add the user to the database
            flash("User successfully created", "info")
            responce = get_redirect()
            if responce is not None:
                return redirect(responce)
            return redirect(url_for("functions.home")) #send the user to the homepage to be redirected
        if request.form["create_user"] == "no":
            return redirect(url_for("functions.login"))
        else:
            flash("Please tick yes or no", "warning")
    return render_template("/user/create.html",username=session["username"])

@user_bp.route("/update/", methods=["POST","GET"])
def user_update():
    if "username" not in session:
        session["redirect"] = "user_update"
        return redirect(url_for("functions.login"))
    if request.method == "POST":
        new_user = list(users_db.select_max(session["username"], 1, session["password"],2)[0])
        print(new_user[2])
        new_user[2] = request.form["roles"]
        print(new_user)
        if "select_args" not in session:
            session["select_args"] = [session["username"], 1, session["password"],2]
        
        users_db.update_max(session["username"],1, session["password"],2,request.form["roles"],3)
        flash(f"Successfully updated user: \'{session['username']}\' to role: \'{request.form['roles']}\'","info")
        return redirect(url_for("functions.home"))
    return render_template("/user/update.html",roles=roles)
