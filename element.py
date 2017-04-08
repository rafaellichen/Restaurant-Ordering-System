import pandas
import numpy

def get_balance(uid):
    users_database = pandas.read_csv("data/users.csv")
    users_balance_database = users_database["balance"].values
    users_uid_database = users_database["uid"].values
    i=0
    for e in users_uid_database:
        if e == uid:
            return users_balance_database[i]
        i+=1

def get_pending_registrations():
    users_database = pandas.read_csv("data/users.csv")
    users_approved_database = users_database["approved"].values
    users_username_database = users_database["username"].values
    temp_list = []
    i=0
    for s in users_approved_database:
        if s == 0:
            temp_list.append(users_username_database[i])
        i+=1
    return temp_list

def get_pending_complaints():
    complaints_database = pandas.read_csv("data/complaints.csv")
    complaints_approval_database = complaints_database["approval"].values
    complaints_cnid_database = complaints_database["cnid"].values
    temp_list = []
    i=0
    for c in complaints_approval_database:
        if c == 0:
            temp_list.append(complaints_cnid_database[i])
        i+=1
    return temp_list

def get_pending_compliments():
    compliments_database = pandas.read_csv("data/compliments.csv")
    compliments_approval_database = compliments_database["approval"].values
    compliments_cpid_database = compliments_database["cpid"].values
    temp_list = []
    i=0
    for c in compliments_approval_database:
        if c == 0:
            temp_list.append(compliments_cpid_database[i])
        i+=1
    return temp_list

def get_comment_content(id,num):
    if num == 1:
        compliments_database = pandas.read_csv("data/compliments.csv")
        comment_database = compliments_database["comment"].values
        cpid_database = compliments_database["cpid"].values
        i=0
        for c in cpid_database:
            if c == int(id):
                return comment_database[i]
            i+=1
    else:
        complaints_database = pandas.read_csv("data/complaints.csv")
        comment_database = complaints_database["comment"].values
        cnid_database = complaints_database["cnid"].values
        i=0
        for c in cnid_database:
            if c == int(id):
                return comment_database[i]
            i+=1

def get_comment_dish(id,num):
    if num==1:
        compliments_database = pandas.read_csv("data/compliments.csv")
        cpid_database = compliments_database["cpid"].values
        compliments_did_database = compliments_database["did"].values
        dish_database = pandas.read_csv("data/dish.csv")
        dish_did_database = dish_database["did"].values
        dish_path_database = dish_database["path"].values
        i=0
        j=0
        did=-1
        for c in cpid_database:
            if c == id:
                did = compliments_did_database[i]
            i+=1
        for d in dish_did_database:
            if d == did:
                print(dish_path_database[j])
                return dish_path_database[j]
            j+=1
    else:
        pass
        