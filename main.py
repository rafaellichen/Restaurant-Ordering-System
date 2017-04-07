from tkinter import *
from tkinter import messagebox
import time
import threading
import queue
import sys
from os import system

import signin
import forget
import bar

program = Tk()
program.title("Restaurant Ordering System")
program.resizable(width=False, height=False)

menubar = Menu(program)
chef_list = Menu(menubar, tearoff=0)
temp_chefs_in_list = bar.chef_in_list()
for e in temp_chefs_in_list:
    chef_list.add_command(label=str(e), command=lambda e=str(e): bar.change_menu(e))
    print(str(e))
menubar.add_cascade(label="Chefs", menu=chef_list)
program.config(menu=menubar)

#variables
class user:
    def __init__(self):
        self.user_level = 0
        self.shopping_cart = []
        self.current_menu = []
        self.top_menu = []

global current_user
current_user = user()

def reset_gui():
    signin_username_label.grid_remove()
    signin_password_label.grid_remove()
    signin_username_entry.grid_remove()
    signin_password_entry.grid_remove()
    signin_confirm_button.grid_remove()
    signin_forget_button.grid_remove()
    signin_forget_label.grid_remove()
    signin_forget_entry.grid_remove()
    signin_forget_button.grid_remove()
    signin_retrive_button.grid_remove()
    signin_back_button.grid_remove()
    forget_back_button.grid_remove()
    signin_username_entry.delete(0,END)
    signin_password_entry.delete(0,END)
    signin_forget_entry.delete(0,END)
    dish_image1.grid_remove()
    dish_image2.grid_remove()
    dish_image3.grid_remove()
    dish_image4.grid_remove()
    dish_image5.grid_remove()
    dish_image6.grid_remove()
    dish_name1.grid_remove()
    dish_name2.grid_remove()
    dish_name3.grid_remove()
    dish_name4.grid_remove()
    dish_name5.grid_remove()
    dish_name6.grid_remove()
    dish_buy1.grid_remove()
    dish_buy2.grid_remove()
    dish_buy3.grid_remove()
    dish_buy4.grid_remove()
    dish_buy5.grid_remove()
    dish_buy6.grid_remove()
    dish_price1.grid_remove()
    dish_price2.grid_remove()
    dish_price3.grid_remove()
    dish_price4.grid_remove()
    dish_price5.grid_remove()
    dish_price6.grid_remove()
    next_page_button.grid_remove()
    previous_page_button.grid_remove()
    signout_status_button.grid_remove()
    signin_status_button.grid_remove()
    balance_label.grid_remove()
    shopping_cart_items.grid_remove()

def window_center():
    program.update()
    # lines below this:
    x = program.winfo_screenwidth()/2 - program.winfo_width()/2
    y = program.winfo_screenheight()/2 - program.winfo_height()/2
    program.geometry("+%d+%d" % (x, y))
    # referenced from: https://bbs.archlinux.org/viewtopic.php?id=149559
    # author: vadmium
    # modified

def signin_confirm_button_action():
    signin_confirm_result = signin.validate(signin_username_entry.get(),signin_password_entry.get())
    # write function to change the software interface based on the type of user
    # replace print command
    if signin_confirm_result == False:
        messagebox.showinfo("","Username or Password is incorrect")
        signin_username_entry.delete(0,END)
        signin_password_entry.delete(0,END)
    elif signin_confirm_result == 1:
        current_user.user_level = 1
        start_interface()
    elif signin_confirm_result == 2:
        current_user.user_level = 2
        start_interface()
    elif signin_confirm_result == 3:
        current_user.user_level = 3
        start_interface()
    elif signin_confirm_result == 4:
        current_user.user_level = 4
        start_interface()
    elif signin_confirm_result == 5:
        current_user.user_level = 5
        start_interface()

def signin_forget_button_action():
    reset_gui()
    signin_forget_label.grid(row=0, column=0)
    signin_forget_entry.grid(row=0, column=1)
    signin_retrive_button.grid(row=1, column=1)
    forget_back_button.grid(row=1, column=0)
    window_center()

def signin_retrieve_button_action():
    signin_retrive_result = forget.retrieve(signin_forget_entry.get())
    messagebox.showinfo("",signin_retrive_result)

def signout_status_button_action():
    current_user.user_level = 0
    shopping_cart = []
    start_interface()  

def signin_interface():
    reset_gui()
    signin_username_label.grid(row=0, column=0)
    signin_password_label.grid(row=1, column=0)
    signin_username_entry.grid(row=0, column=1)
    signin_password_entry.grid(row=1, column=1)
    signin_confirm_button.grid(row=2, column=1)
    signin_forget_button.grid(row=2, column=0)
    signin_back_button.grid(row=2, column=2)
    window_center()

def start_interface():
    reset_gui()
    if(current_user.user_level == 0):
        signin_status_button.grid(row=0, column=2)
    else:
        signout_status_button.grid(row=0, column=2)
        balance_label.grid(row=0, column=0)
    shopping_cart_items.grid(row=0, column=1)
    dish_image1.grid(row=1, column=0)
    dish_name1.grid(row=2, column=0)
    dish_price1.grid(row=3, column=0)
    dish_buy1.grid(row=4, column=0)
    dish_image2.grid(row=1, column=1)
    dish_name2.grid(row=2, column=1)
    dish_price2.grid(row=3, column=1)
    dish_buy2.grid(row=4, column=1)
    dish_image3.grid(row=1, column=2)
    dish_name3.grid(row=2, column=2)
    dish_price3.grid(row=3, column=2)
    dish_buy3.grid(row=4, column=2)
    dish_image4.grid(row=5, column=0)
    dish_name4.grid(row=6, column=0)
    dish_price4.grid(row=7, column=0)
    dish_buy4.grid(row=8, column=0)
    dish_image5.grid(row=5, column=1)
    dish_name5.grid(row=6, column=1)
    dish_price5.grid(row=7, column=1)
    dish_buy5.grid(row=8, column=1)
    dish_image6.grid(row=5, column=2)
    dish_name6.grid(row=6, column=2)
    dish_price6.grid(row=7, column=2)
    dish_buy6.grid(row=8, column=2)
    next_page_button.grid(row=9, column=2)
    previous_page_button.grid(row=9, column=0)
    window_center()

def menu_next_page():
    pass

def menu_previous_page():
    pass    

#signin interface
signin_username_label = Label(program, text="Username")
signin_password_label = Label(program, text="Password")
signin_username_entry = Entry(program)
signin_password_entry = Entry(program)
signin_confirm_button = Button(text="Sign in", command=signin_confirm_button_action)
signin_forget_button = Button(text="Forget", command=signin_forget_button_action)
signin_back_button = Button(text="Back", command=start_interface)

#forget interface
signin_forget_entry = Entry(program)
signin_forget_label = Label(program, text="Email")
signin_retrive_button = Button(text="Retrive", command=signin_retrieve_button_action)
forget_back_button = Button(text="Back", command=signin_interface)

#start interface
balance_label = Label(program, text="Balance")
shopping_cart_items = Label(program, text=str(len(current_user.shopping_cart)))
signout_status_button = Button(text="Sign Out", command=signout_status_button_action)
signin_status_button = Button(text="Sign In", command=signin_interface)
next_page_button = Button(text="Next", command=menu_next_page)
previous_page_button = Button(text="Previous", command=menu_previous_page)
etc_photo = PhotoImage(file="images/etc.gif")
dish_image1 = Label(image=None)
dish_name1 = Label(program, text="Name")
dish_price1 = Label(program, text="Price")
dish_buy1 = Button(text="Add to cart", command=None)
dish_did1=""
dish_image2 = Label(image=None)
dish_name2 = Label(program, text="Name")
dish_price2 = Label(program, text="Price")
dish_buy2 = Button(text="Add to cart", command=None)
dish_did2=""
dish_image3 = Label(image=None)
dish_name3 = Label(program, text="Name")
dish_price3 = Label(program, text="Price")
dish_buy3 = Button(text="Add to cart", command=None)
dish_did3=""
dish_image4 = Label(image=None)
dish_name4 = Label(program, text="Name")
dish_price4 = Label(program, text="Price")
dish_buy4 = Button(text="Add to cart", command=None)
dish_did4=""
dish_image5 = Label(image=None)
dish_name5 = Label(program, text="Name")
dish_price5 = Label(program, text="Price")
dish_buy5 = Button(text="Add to cart", command=None)
dish_did5=""
dish_image6 = Label(image=None)
dish_name6 = Label(program, text="Name")
dish_price6 = Label(program, text="Price")
dish_buy6 = Button(text="Add to cart", command=None)
dish_did6=""

def test():
    dish_image1.config(image=etc_photo)
    dish_image2.config(image=etc_photo)
    dish_image3.config(image=etc_photo)
    dish_image4.config(image=etc_photo)
    dish_image5.config(image=etc_photo)
    dish_image6.config(image=etc_photo)

start_interface()
test()
window_center()
program.mainloop()