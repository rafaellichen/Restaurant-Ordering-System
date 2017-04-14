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
                    users_database.set_value(i, "balance", 0)
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

def demote_promote_employee(uid,a):
    salary_file = pandas.read_csv("data/salary.csv")
    salary_current = salary_file["salary"].values
    uid_list = salary_file["uid"].values
    i=0
    if a == 1:
        for e in uid_list:
            if e == int(uid):
                salary_file.set_value(i, "salary", salary_current[i]+25)
                messagebox.showinfo("", "Promoted.\nSalary is increased by 25")
            i+=1
    else:
        for e in uid_list:
            if e == int(uid):
                salary_file.set_value(i, "salary", salary_current[i]-25)
                messagebox.showinfo("", "Demoted.\nSalary is reduced by 25")
            i+=1
    salary_file.to_csv("data/salary.csv", index=False)

def auto_demote_promote_employee():
    auto_fire = []
    salary_file = pandas.read_csv("data/salary.csv")
    users_file = pandas.read_csv("data/users.csv")
    uid = salary_file["uid"].values
    demoted_time = salary_file["demoted"].values
    i=0
    for e in demoted_time:
        if e == 2:
            users_file.set_value(uid[i], "approved", -1)
        i+=1
    salary_current = salary_file["salary"].values
    compliments_time = salary_file["compliments"].values
    complaints_time = salary_file["complaints"].values
    demoted_current = salary_file["demoted"].values
    time = []
    for e,f in zip(compliments_time, complaints_time):
        time.append(e-f)
    i=0
    for e in time:
        if e >= 3:
            salary_file.set_value(i, "salary", salary_current[i]+50)
            salary_file.set_value(i, "compliments", 0)
            salary_file.set_value(i, "complaints", 0)
            salary_file.set_value(i, "demoted", demoted_current[i]-1)
        elif e <= -3:
            salary_file.set_value(i, "salary", salary_current[i]-50)
            salary_file.set_value(i, "compliments", 0)
            salary_file.set_value(i, "complaints", 0)
            salary_file.set_value(i, "demoted", demoted_current[i]+1)
        i+=1
    salary_file.to_csv("data/salary.csv", index=False)
    users_file.to_csv("data/users.csv", index=False)

def auto_vip_block():
    user_file = pandas.read_csv("data/users.csv")
    spent = user_file["spent"].values
    orders = user_file["orders"].values
    warnings = user_file["warning"].values
    level = user_file["level"].values
    i=0
    for e,f in zip(warnings,level):
        if not numpy.isnan(e) and e>=2 and f==2:
            user_file.set_value(i, "level", 1)
            user_file.set_value(i, "spent", 0)
            user_file.set_value(i, "orders", 0)
            user_file.set_value(i, "warning", 0)
        if not numpy.isnan(e) and e>=3 and f==1:
            user_file.set_value(i, "approved", -1)
            user_file.set_value(i, "warning", 0)
        i+=1
    i=0
    for e,f in zip(spent,orders):
        if (not numpy.isnan(e) and e>=500) or (not numpy.isnan(f) and f>=50):
            user_file.set_value(i, "level", 2)
            user_file.set_value(i, "spent", 0)
            user_file.set_value(i, "orders", 0)
        i+=1
    user_file.to_csv("data/users.csv", index=False)

