from flask import Blueprint, render_template, session, url_for, request, redirect, flash
import database_mod
from info import admin_roles

notes_bp = Blueprint("notes", __name__,
    template_folder="templates")

notes_db = database_mod.db("main.db","notes") #set where the database is reading from
notes_db.setup("username","title","note","password") #set up the columns in the database


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
        session["current_note"] = list(note[0]) # get it from the database
        return redirect(url_for("challenges.notes.view")) #redirect to the viewing page
    if session["role"] in admin_roles: # if the user is an admin
        return render_template("challenges/notes/home.html", notes=notes_db.read()) # get notes from all users
    return render_template("challenges/notes/home.html", notes=notes_db.select(session["username"],1)) #load the home page

@notes_bp.route("/view/", methods=["POST","GET"])
def view():
    if "current_note" not in session: #if the user has not picked a text to edit
        return redirect(url_for("challenges.notes.home")) #send them to the home page to pick
    if request.method == "POST":
        print(request.form)
        notes_db.update_two_val_two_cond(session["current_note"][0],1, session["current_note"][1],2, request.form["title"],2, request.form["return_text"],3)
        return redirect(url_for("challenges.notes.home"))
    return render_template("challenges/notes/new_note.html",text=session["current_note"])

@notes_bp.route("/new/", methods=["POST", "GET"])
def new_note():
    if "username" not in session: #if the user is not logged in
        session["redirect"] = "challenges.notes.new_note" #set the return address
        return redirect(url_for("functions.login")) #send the user to the login page
    if request.method == "POST": # if the user has returned the form to save the page
        title = request.form["title"] #get the users title
        note_text = request.form["return_text"] #get the users text
        print(note_text) #print to check formatting
        notes_db.insert(session["username"], title, note_text, "") #save it to the database
        return redirect(url_for("challenges.notes.home"))#return to the homepage
    return render_template("challenges/notes/new_note.html") #load the page