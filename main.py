from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from tabulate import tabulate
from info import allow_blank_passwords
import info
import hashlib
import database

app = Flask(__name__)
app.secret_key = "something to say about nothing"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

str = database.db("main.db","users")
users_db.setup("username","password", "role")

addresses = {}

def hash(str):
    salt = "2d1133dd810c6ca8e84118c79545847b"
    hashed = hashlib.md5(str.encode()+salt.encode())
    return hashed.hexdigest()

def get_redirect(redirect_arg=False):
    if "redirect" not in session:
        session["redirect"] = None

    if session["redirect"] is not None:
        redirect = session["redirect"]
        if redirect_arg:
            session["redirect"] = None
        return url_for(redirect)
    return None

@app.route("/")
@app.route("/home/")
def home():
    if "username" in session:
        session["select_args"] = [session["username"], 1, session["password"],2]
        return render_template("menu/home.html")
    return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("home"))



@app.route("/login/",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username.strip()) == 0 or len(password.strip()) == 0 and not allow_blank_passwords:
            flash("Do not leave usernames or passwords blank","warning")
            return render_template("/menu/login.html")
        session["username"] = username
        session["password"] = hash(password)
        
        if len(users_db.select_max(*sesssession["username"], 1, session["password"],2) :
            if get_redirect() is not None:
                session["logged in"] = True
                flash(f"logged in as user {username}", "info")
                return redirect(url_for("home"))
            return redirect(get_redirect(True))
        return redirect(url_for("user_create"))

    return render_template("/menu/login.html")

#-----------------database----------------------------

@app.route("/database/")
def database_home():
    return render_template("/database/home.html")

@app.route("/database/list/")
def database_list():
    return render_template("/database/list.html",users=users_db.read(), headings=users_db.columns())

@app.route("/database/clear/", methods=["POST","GET"])
def database_clear():
    if request.method == "POST":
        if request.form["answer"] == "yes":
            users_db.clear()
        return redirect(url_for("logout"))
    return render_template("/database/clear.html")

#----------------user--------------------------
@app.route("/user/")
def user_home():
    return render_template("/user/home.html")

@app.route("/user/create/", methods=["POST","GET"])
def user_create():
    if "username" not in session: #if the user hasnt tryed to login
        return redirect(url_for("login")) # get the users username and password
    if len(users_db.select_max(session["username"], 1, session["password"],2)) != 0: #see if the user account already exists
        return redirect(url_for("home")) # return to the home page to be redirected
    if request.method == "POST":
        if request.form["create_user"] == "yes": #make sure the user wants to create the user
            users_db.insert(session["username"], session["password"], info.defualt_role) #add the user to the database
            flash("User successfully created", "info")
            return redirect(url_for("home")) #send the user to the homepage to be redirected
        if request.form["create_user"] == "no":
            return redirect(url_for("login"))
        else:
            flash("Please tick yes or no", "warning")
    return render_template("/user/create.html",username=session["username"])

@app.route("/user/update/", methods=["POST","GET"])
def user_update():
    if "username" not in session:
        session["redirect"] = "user_update"
        return redirect(url_for("login"))
    if request.method == "POST":
        new_user = list(users_db.select_max(session["username"], 1, session["password"],2)[0])
        print(new_user[2])
        new_user[2] = request.form["roles"]
        print(new_user)
        if "select_args" not in session:
            
        users_db.update_max(session["username"],1, session["password"],2,request.form["roles"],3)
        return str(user_db.select_max(*sesson["select_args"]))
        
        return request.form["roles"]
    return render_template("/menu/update.html",roles=info.roles)


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0")