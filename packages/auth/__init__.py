from flask import session
import random
from packages.database import AddDoc, ReadDoc

def SignupUser(email, password, username, type):
    canRegister = False

    verifyEmailDoc = ReadDoc("users.txt")
    emailsUsers = []

    if verifyEmailDoc == []:
        canRegister = True

    for pk, columns, values in verifyEmailDoc:
        emailsUsers.append(values[1])

    for verifyEmail in range(len(emailsUsers)):
        print(verifyEmail)
        if email == emailsUsers[verifyEmail]:
            return False
        else:
            canRegister = True

    if canRegister:
        data_user = {
            "username": username,
            "email": email,
            "password": password,
            "type": type,
            "profile_picture": "/static/profile_picture.png"
        }

        if AddDoc("users.txt", random.randint(9999, 1000000), data_user):
            return True
        else:
            return False
    else:
        return False

def SigninUser(email, password):
    users = ReadDoc("users.txt")

    notFoundUser = False

    for id, columns, values in users:
        if email == values[1] and password == values[2]:
            username, email_, password_, typeUser, profile_picture = values
            #session["session"] = [username, typeUser, profile_picture]
            session["session"] = {
                "uid": id,
                "username": username,
                "typeUser": typeUser,
                "email": email,
                "profile_picture": profile_picture
            }

            return True
        else:
            notFoundUser = True

    if notFoundUser:
        return False
        
def LogoutUser():
    if "session" in session:
        session.pop("session", None)
        return True
    else:
        return False
    
def VerifySession():
    if "session" in session:
        return True
    else:
        return False