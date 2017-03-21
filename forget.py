import pandas
import numpy
import smtplib

def retrieve(email_input):
    users_database = pandas.read_csv("users.csv")
    users_username_database = users_database["username"].values
    users_password_database = users_database["password"].values
    users_email_database = users_database["email"].values
    i=0
    for email_check in users_email_database:
        if email_check == email_input:
            return (users_username_database[i],",",users_password_database[i])
        i+=1
    return ("?",",","?")