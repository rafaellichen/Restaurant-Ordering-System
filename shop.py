import pandas
import numpy
from tkinter import messagebox
from collections import Counter

def check_quantity(input):
    if input == "":
        messagebox.showinfo("", "Please enter valid integer")
        return False
    if input.isdigit():
        if int(input) >=0:
            return True
        else:
            messagebox.showinfo("", "Please enter valid integer")
            return False
    else:
        messagebox.showinfo("", "Please enter valid integer")
        return False

def get_list(a):
    did_list = [int(float(x)) for x in a]
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

def write_cart(uid,cart):
    if uid != -1:
        cart_str = ""
        for e in cart:
            cart_str+=str(e)+","
        cart_str=str(cart_str[:-1])
        cart_database = pandas.read_csv("data/users.csv")
        cart_database.loc[cart_database["uid"]==uid, "cart"]=cart_str
        cart_database.to_csv("data/users.csv", index=False)

def get_cart(uid):
    cart_database = pandas.read_csv("data/users.csv")
    cart_database = cart_database.loc[cart_database["uid"]==uid]["cart"].values
    temp = []
    try:
        if not numpy.isnan(cart_database[0]):
            try:
                temp = cart_database[0].split(",")
            except AttributeError:
                temp = [cart_database[0]]
    except TypeError:
        temp = cart_database[0].split(",")
    print(type(temp))
    return temp

def checkout_balance(level, total, uid):
    if level != 1 and level != 2:
        return False
    data_file = pandas.read_csv("data/users.csv")
    balance = (data_file.loc[data_file["uid"]==uid]["balance"].values)[0]
    if balance >= total:
        if level == 2:
            result = messagebox.askyesno("Confirm payment","Discounted price: "+str(int((total*0.9))))
            if result:
                data_file.loc[data_file["uid"]==uid, "balance"]=balance-int((total*0.9))
                data_file.loc[data_file["uid"]==uid, "cart"] = numpy.nan
                data_file.to_csv("data/users.csv", index=False)
                return True
        if level == 1:
            result = messagebox.askyesno("Confirm payment","Final price: "+str(int((total))))
            if result:
                print(balance-total)
                data_file.loc[data_file["uid"]==uid, "balance"]=balance-total
                data_file.loc[data_file["uid"]==uid, "cart"] = numpy.nan
                data_file.to_csv("data/users.csv", index=False)
                return True
    else:
        messagebox.showinfo("","Not enough balance")
    return False

def write_order(uid, cart):
    data_file = pandas.read_csv("data/order.csv")
    ddid = data_file["ddid"].values.tolist()
    order = data_file["order"].values.tolist()
    destination = data_file["destination"].values.tolist()
    status = data_file["status"].values.tolist()
    uid_data = data_file["uid"].values.tolist()
    rate = data_file["rate"].values.tolist()
    rated = data_file["rated"].values.tolist()
    ddid.append(ddid[-1]+1)
    cart_str = ""
    for e in cart:
        cart_str+=str(int(e))+","
    cart_str=cart_str[:-1]
    order.append(cart_str)
    destination.append(numpy.nan)
    status.append(-1)
    uid_data.append(uid)
    rate.append(0)
    rated.append(0)
    order_database = pandas.DataFrame({"ddid": ddid,
                                        "order": order,
                                        "destination": destination,
                                        "status": status,
                                        "uid": uid_data,
                                        "rate": rate,
                                        "rated": rated})
    order_database = order_database[["ddid",
                                    "order",
                                    "destination",
                                    "status",
                                    "uid",
                                    "rate",
                                    "rated"]]
    order_database.to_csv("data/order.csv", index=False)