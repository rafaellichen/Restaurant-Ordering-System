import pandas
import numpy

def validate(username_input,password_input):
    users_database = pandas.read_csv("users.csv")
    users_username_database = users_database["username"].values
    users_password_database = users_database["password"].values
    users_level_database = users_database["level"].values
    i=0
    for username_check in users_username_database:
        if username_check == username_input:
            if users_password_database[i] == password_input:
                return users_level_database[i]
            else:
                return False
        i+=1
    return False