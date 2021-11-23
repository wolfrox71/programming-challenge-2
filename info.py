#login
allow_blank_passwords = False #allows the user to have a password consisting of just spaces

#create user
defualt_role = "user"
roles=["user","admin"]
admin_roles=["admin"]

#hash
import hashlib
def hash(str):
    salt = "2d1133dd810c6ca8e84118c79545847b"
    hashed = hashlib.sha256(str.encode()+salt.encode())
    return hashed.hexdigest()


#get_redirect
from flask import session, url_for
def get_redirect():
    if "redirect" not in session: #see if the user has added a redirect
        session["redirect"] = None #set it to none

    if session["redirect"] is not None: #if there is a valid url
        redirect_addr = session["redirect"] #get the url in a variable
        session["redirect"] = None #remove the url from session
        return url_for(redirect_addr) #return the url for the sessioned url
    return None #return None if the is not a url
"""
use ->
from info import get_redirect
responce = get_redirect() #wipes the url after the function call so needs to be caught
if responce is not None: #returns None if there is no url
    return redirect(responce) #return to the specified url
"""