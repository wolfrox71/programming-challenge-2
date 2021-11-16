from flask import Flask, session, url_for
from datetime import timedelta
from database.database import database_bp
from user.user import user_bp
from functions.functions import functions_bp
from challenges.challenges import challenges_bp
import database_mod

app = Flask(__name__)
app.secret_key = "something to say about nothing"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)
users_db = database_mod.db("main.db","users")
users_db.setup("username","password", "role")

app.register_blueprint(database_bp, url_prefix="/database/")
app.register_blueprint(user_bp, url_prefix="/user/")
app.register_blueprint(functions_bp, url_prefix="/")
app.register_blueprint(challenges_bp, url_prefix="/game/")
addresses = {}

def get_redirect(redirect_arg=False):
    if "redirect" not in session:
        session["redirect"] = None

    if session["redirect"] is not None:
        redirect = session["redirect"]
        if redirect_arg:
            session["redirect"] = None
        return url_for(redirect)
    return None

@app.route("/map/")
def game():
    return str(app.url_map)
    
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0")