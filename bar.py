import pandas
import numpy

def chef_in_list():
    chefs = pandas.read_csv("data/users.csv")
    chefs = chefs.loc[chefs["level"]==4]
    return chefs["name"].values

def change_menu(chef):
    if chef=="A":
        print("A")
    elif chef=="B":
        print("B")
    elif chef=="C":
        print("C")