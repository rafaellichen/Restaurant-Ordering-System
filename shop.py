import pandas
import numpy
from tkinter import messagebox
from collections import Counter

def check_quantity(input):
    if input == "":
        messagebox.showinfo("", "Please enter valid integer")
        return False
    if input.isdigit():
        if int(input) >0:
            return True
        else:
            messagebox.showinfo("", "Please enter valid integer")
            return False
    else:
        messagebox.showinfo("", "Please enter valid integer")
        return False

def order_summary():
    pass

def get_list(a):
    did_list = [int(x) for x in a]
    count = Counter(did_list)
    return count.most_common()

def name_list(l):
    name_database = pandas.read_csv("data/dish.csv")
    name = name_database["dish"].values
    did = name_database["did"].values
    price = name_database["price"].values
    path = name_database["path"].values
    return_name = []
    return_price = []
    return_image = []
    for f in l:
        i=0
        for e,a,p,pa in zip(did,name,price,path):
            if e == f:
                return_name.append(a)
                return_price.append(p)
                return_image.append(pa)
        i+=1
    return (return_name, return_price, return_image)