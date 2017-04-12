import pandas
import numpy
from collections import Counter

def get_balance(uid):
    users_database = pandas.read_csv("data/users.csv")
    users_balance_database = users_database["balance"].values
    users_uid_database = users_database["uid"].values
    i=0
    for e in users_uid_database:
        if e == uid:
            return users_balance_database[i]
        i+=1

def get_order_list():
    order_database = pandas.read_csv("data/order.csv")
    order_statues = order_database["status"].values
    order_number = order_database["ddid"].values
    temp_orderlist = []
    i=0
    for x in order_statues:
        if x == -1:
            temp_orderlist.append(order_number[i])
        i+=1
    return temp_orderlist

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

def get_comment(t, num):
    if t == 1:
        compliments_database = pandas.read_csv("data/compliments.csv")
        compliments_database = compliments_database.loc[compliments_database["approval"] == num]
        return compliments_database["cpid"].values
    else:
        complaints_database = pandas.read_csv("data/complaints.csv")
        complaints_database = complaints_database.loc[complaints_database["approval"] == num]
        return complaints_database["cnid"].values

def get_users(num):
    if num == 0:
        approved_database = pandas.read_csv("data/users.csv")
        return approved_database["username"].values
    else:
        approved_database = pandas.read_csv("data/users.csv")
        approved_database = approved_database.loc[approved_database["approved"] == num]
        return approved_database["username"].values

def get_menu_list():
    did_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(did_database.sort_values("time")["did"].values)))

def get_image_list():
    path_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(path_database.sort_values("time")["path"].values)))

def get_name_list():
    name_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(name_database.sort_values("time")["dish"].values)))

def get_price_list():
    price_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(price_database.sort_values("time")["price"].values)))

def get_top_listing(uid):
    delivery_database = pandas.read_csv("data/order.csv")
    delivery_database = delivery_database.loc[delivery_database["uid"] == uid]
    delivery_database = delivery_database.loc[delivery_database["status"] == 1]
    did_list = []
    for e in delivery_database["order"].values:
        did_list+=e.split(",")
    did_list = [int(x) for x in did_list]
    count = Counter(did_list)
    did_list = sorted(sorted(did_list), key=count.get, reverse=True)
    set_did_list = []
    for e in did_list:
        if len(set_did_list) == 0:
            set_did_list.append(e)
        else:
            if set_did_list[-1] != e:
                set_did_list.append(e)
    return set_did_list