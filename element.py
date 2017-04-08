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