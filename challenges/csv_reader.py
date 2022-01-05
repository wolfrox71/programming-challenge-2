from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

csv_reader_bp = Blueprint("csv_reader", __name__,
    template_folder="templates")

@csv_reader_bp.route("/", methods=["POST","GET"])
def home():
    session["csv_file_save"] = "/challenges/templates/challenges/csv_reader/file_save/"
    if request.method == "POST": 
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files["file"]
        if file.filename =="":
            flash("Please upload a file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(session["csv_file_Save"],filename))
        return request.form["file"]
    return render_template("challenges/csv_reader/home.html")