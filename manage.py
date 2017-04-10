import pandas
import numpy
from tkinter import *
from tkinter import messagebox

def approve_pending_registrations(username, input):
    users_database = pandas.read_csv("data/users.csv")
    users_username_database = users_database["username"].values
    users_balance_database = users_database["balance"].values
    i=0
    for u in users_username_database:
        if u == username:
            if input == 1:
                result = messagebox.askyesno("","Approving the following user:\n"+"Username: "+str(username)+
                                                "\nBalance: $"+str(users_balance_database[i]))
                if result:
                    users_database.set_value(i, "approved", 1)
                    users_database.to_csv("data/users.csv", index=False)
            else:
                result = messagebox.askyesno("","Declining the following user:\n"+"Username: "+str(username)+
                                                "\nBalance: $"+str(users_balance_database[i]))
                if result:
                    users_database.set_value(i, "approved", -1)
                    users_database.to_csv("data/users.csv", index=False)
        i+=1

def approve_compliments(cpid, input):
    compliments_database = pandas.read_csv("data/compliments.csv")
    compliments_cpid_database = compliments_database["cpid"].values
    compliments_comment_database = compliments_database["comment"].values
    i=0
    for c in compliments_cpid_database:
        if c == int(cpid):
            if input == 1:
                result = messagebox.askyesno("","Approving the following comment:\n"+str(compliments_comment_database[i]))
                if result:
                    compliments_database.set_value(i, "approval", 1)
                    compliments_database.to_csv("data/compliments.csv", index=False)
            else:
                result = messagebox.askyesno("","Declining the following comment:\n"+str(compliments_comment_database[i]))
                if result:
                    compliments_database.set_value(i, "approval", -1)
                    compliments_database.to_csv("data/compliments.csv", index=False)
        i+=1

def approve_complaints(cnid, input):
    complaints_database = pandas.read_csv("data/complaints.csv")
    complaints_cnid_database = complaints_database["cnid"].values
    complaints_comment_database = complaints_database["comment"].values
    i=0
    for c in complaints_cnid_database:
        if c == int(cnid):
            if input == 1:
                result = messagebox.askyesno("","Approving the following comment:\n"+str(complaints_comment_database[i]))
                if result:
                    complaints_database.set_value(i, "approval", 1)
                    complaints_database.to_csv("data/complaints.csv", index=False)
            else:
                result = messagebox.askyesno("","Declining the following comment:\n"+str(complaints_comment_database[i]))
                if result:
                    complaints_database.set_value(i, "approval", -1)
                    complaints_database.to_csv("data/complaints.csv", index=False)
        i+=1