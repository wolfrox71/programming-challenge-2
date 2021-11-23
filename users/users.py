from flask import Blueprint, render_template, redirect, request, url_for, flash, session
import database_mod
from info import admin_roles 

users_bp = Blueprint("users", __name__,
    template_folder="templates")

users_db = database_mod.db("main.db","users") #init the database class
users_db.setup("username","password", "role") #setup the database -> hopefully isnt needed but just incase it should still work

@users_bp.route("/")
def user_home():
    return render_template("/users/home.html")

@users_bp.route("/delete/",methods=["POST","GET"])
def users_delete():
    if "username" not in session: #if the user is not logged in
        session["redirect"] = "users.users_delete" #make the user return to this page when they have logged in
        return redirect(url_for("functions.login")) #send them to login
    if users_db.select_max(*session["select_args"])[0][2] not in admin_roles: #if the user is not an admin
        flash("Need to be admin")
        return redirect(url_for("functions.home")) #send them to the home page
    
    if request.method == "POST": #if they send a form
        #request.form return the username and password of the selected user
        users_db.remove_max(request.form["to_del"].split("¦|")[0],1,request.form["to_del"].split("¦|")[1],2) #delete the user with the returned username and password
        return redirect(url_for("functions.logout")) #returns the user to the logout page to fix errors w\ deleting the logged in user

    return render_template("/users/delete.html",users=users_db.read()) #display the delete page with the users in the database as arguments