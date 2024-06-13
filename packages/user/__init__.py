from packages.database import *

def GetUserData(uid):
    users = ReadDoc("users.txt")

    user_data = {}

    for pk, columns, values in users:
        if str(uid) == str(pk):
            user_data = {
                "uid": pk,
                "username": values[0],
                "email": values[1],
                "typeUser": values[3],
                "profile_picture": values[4]
            }

            break

    return user_data

def GetUserTickets(uid):
    return "a"