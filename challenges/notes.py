from flask import Blueprint, render_template, session, url_for, request, redirect, flash
import database_mod
from info import admin_roles, hash

notes_bp = Blueprint("notes", __name__,
    template_folder="templates")

notes_db = database_mod.db("main.db","notes") #set where the database is reading from
notes_db.setup("username","title","note","password") #set up the columns in the database

@notes_bp.route("/view/", methods=["POST","GET"])
@notes_bp.route("/", methods=["POST","GET"])
def home():
    if "username" not in session: #if the user is not logged in
        session["redirect"] = "challenges.notes.home" #set a return adress
        return redirect(url_for("functions.login")) #log them in 
    if request.method == "POST": #if the user has picked a note to edit
        username, title = request.form["picked_note"].split("¦|") #get the user and the return notes title
        if "" in [username]:# this is so that the database does not break
            flash("Select a note", "info") #send a message to stop the user sending a blank input again
            return redirect(url_for("challenges.notes.home")) #reload the page
        note = notes_db.select_max(username,1, title,2) 
        if len(note) == 0: # if there is no notes with those catagories
            flash("An error occured loading that note", "Error") #this may happen if a note is deleted by one user and another is trying to load it
            return redirect(url_for("challenges.notes.home")) # reload the page
        a = 1
        var = (a==2) if "test" else "something"
        return str(var)
        session["note_password"] = [True, False][notes_db.select_max(username,1, title, 2)[0][-1] == ""] # true if the note is password protected, False if not
        session["current_note"] = list(note[0]) # get it from the database
        if session["note_password"]:
            return redirect(url_for("challenges.notes.password"))
        return redirect(url_for("challenges.notes.read")) #redirect to the reading page
    
    if session["role"] in admin_roles: # if the user is an admin
        return render_template("challenges/notes/home.html", notes=notes_db.read()) # get notes from all users
    return render_template("challenges/notes/home.html", notes=notes_db.select(session["username"],1)) #load the home page

@notes_bp.route("/password/", methods=["POST","GET"])
def password():
    if request.method == "POST":
        return str(request.form)
        if request.form["password"] == notes_db.select_max(session["current_note"][0],1, session["current_note"][1], 2)[0][-1]:
            return redirect(url_for("challenges.notes.read"))

    return """
    <form type="POST" action="#">
    <input type="password">Enter your password</input>
    <br>
    <input type="submit"></input>
    </form>
    """

@notes_bp.route("/read/", methods=["POST","GET"])
def read():
    if request.method == "POST":
        if "username" not in session:
            title = request.form["title"] 
            note_text = request.form["return_text"] #this is so that if the user logs out while writing a document it saves it with the username "logged out"
            notes_db.insert("logged out edit", title, note_text, "") #save it with the username "logged out"
            session["redirect"] = "challenges.notes.read"
            return redirect(url_for("functions.login"))
        
        notes_db.update_max(session["curretn_note"][0],1, session["current_note"][1], 2, hash(request.form["password"])) #update the password and hash it. The password is not checked apart from accessing it so is updated first
        notes_db.update_two_val_two_cond(session["current_note"][0],1, session["current_note"][1],2, request.form["title"],2, request.form["return_text"],3)
        notes_db.update_max(request.form["return_text"],3, request.form["title"],2, request.form["author"],1)
        if session["role"] in admin_roles:
            notes_db.update_max(request.form["return_text"],3, request.form["title"],2, request.form["author"],1)
        return redirect(url_for("challenges.notes.home"))
    if "current_note" not in session: #if the user has not picked a text to edit
        return redirect(url_for("challenges.notes.home")) #send them to the home page to pick
    return render_template("challenges/notes/new_note.html",text=session["current_note"])

@notes_bp.route("/new/", methods=["POST", "GET"])
def new_note():
    if request.method == "POST": # if the user has returned the form to save the page
        title = request.form["title"] #get the users title
        note_text = request.form["return_text"] #get the users text
        password = hash(request.form["password"])
        if "username" not in session: #if the user is not logged in
            notes_db.insert("logged out", title, note_text, "") #save it with the username "logged out", this does not have a password as an admin may need to change the author from "logged out" and so cannot have a password
            return redirect(url_for("challenges.notes.home"))#return to the homepage
    
    
        notes_db.insert(session["username"], title, note_text, password) #save it to the database
        return redirect(url_for("challenges.notes.home"))#return to the homepage
    
    if "username" not in session: #if the user is not logged in
        session["redirect"] = "challenges.notes.new_note" #set the return address
        return redirect(url_for("functions.login")) #send the user to the login page
    return render_template("challenges/notes/new_note.html",text=["","",""]) #load the page

@notes_bp.route("/delete/", methods=["POST","GET"])
def delete():
    if "username" not in session or "role" not in session:
        session["redirect"] = "challenges.notes.delete"
        return redirect(url_for("functions.login"))
    if request.method == "POST":
        username, title = request.form["note_to_del"].split("¦|") 
        if "" in [username]:# this is so that the database does not break
            flash("Select a note", "info") #send a message to stop the user sending a blank input again
            return redirect(url_for("challenges.notes.delete")) #reload the page
        notes_db.remove_max(username,1,title,2)
        return redirect(url_for("challenges.notes.home"))
    if session["role"] in admin_roles:
        return render_template("challenges/notes/delete.html", notes=notes_db.read())
    return render_template("challenges/notes/delete.html", notes=notes_db.select(session["username"],1))