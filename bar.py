import pandas
import numpy

def chef_in_list():
    chefs = pandas.read_csv("data/users.csv")
    chefs = chefs.loc[chefs["level"]==4]
    return (chefs["name"].values, chefs["uid"].values)

def get_menu_list(input):
    did_database = pandas.read_csv("data/dish.csv")
    did_database = did_database.loc[(did_database["uid"]==input) | (did_database["uid"]==-1)]
    return (list(reversed(did_database.sort_values("time")["did"].values)))

def get_image_list(input):
    path_database = pandas.read_csv("data/dish.csv")
    path_database = path_database.loc[(path_database["uid"]==input) | (path_database["uid"]==-1)]
    return (list(reversed(path_database.sort_values("time")["path"].values)))

def get_name_list(input):
    name_database = pandas.read_csv("data/dish.csv")
    name_database = name_database.loc[(name_database["uid"]==input) | (name_database["uid"]==-1)]
    return (list(reversed(name_database.sort_values("time")["dish"].values)))

def get_price_list(input):
    price_database = pandas.read_csv("data/dish.csv")
    price_database = price_database.loc[(price_database["uid"]==input) | (price_database["uid"]==-1)]
    return (list(reversed(price_database.sort_values("time")["price"].values)))