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
    hashed = hashlib.md5(str.encode()+salt.encode())
    return hashed.hexdigest()