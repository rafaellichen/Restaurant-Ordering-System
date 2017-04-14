import pandas
import numpy

def chef_in_list():
    chefs = pandas.read_csv("data/users.csv")
    chefs = chefs.loc[(chefs["level"]==4) & (chefs["approved"]==1)]
    return (chefs["name"].values, chefs["uid"].values)

def get_menu_list(input):
    did_database = pandas.read_csv("data/menu.csv")
    did_database = did_database.loc[(did_database["uid"]==input) | (did_database["uid"]==-1)]
    return (list(reversed(did_database.sort_values("time")["did"].values)))

def get_image_list(input):
    path_database = pandas.read_csv("data/menu.csv")
    path_database = path_database.loc[(path_database["uid"]==input) | (path_database["uid"]==-1)]
    return (list(reversed(path_database.sort_values("time")["path"].values)))

def get_name_list(input):
    name_database = pandas.read_csv("data/menu.csv")
    name_database = name_database.loc[(name_database["uid"]==input) | (name_database["uid"]==-1)]
    return (list(reversed(name_database.sort_values("time")["dish"].values)))

def get_price_list(input):
    price_database = pandas.read_csv("data/menu.csv")
    price_database = price_database.loc[(price_database["uid"]==input) | (price_database["uid"]==-1)]
    return (list(reversed(price_database.sort_values("time")["price"].values)))

def get_top_image_list(input):
    image_list = []
    image_database = pandas.read_csv("data/menu.csv")
    for e in input:
        image_list.append(image_database.loc[image_database["did"]==e]["path"].iloc[0])
    return image_list

def get_top_name_list(input):
    name_list = []
    name_database = pandas.read_csv("data/menu.csv")
    for e in input:
        name_list.append(name_database.loc[name_database["did"]==e]["dish"].iloc[0])
    return name_list

def get_top_price_list(input):
    price_list = []
    price_database = pandas.read_csv("data/menu.csv")
    for e in input:
        price_list.append(price_database.loc[price_database["did"]==e]["price"].iloc[0])
    return price_list