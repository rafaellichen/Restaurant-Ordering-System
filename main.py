from tkinter import *
from tkinter import messagebox
import time
import threading
import queue
import sys
from os import system

import signin
import forget

program = Tk()
program.title("Restaurant Ordering System")
program.resizable(width=False, height=False)

#constants
user_level = 0
menu_display = queue.Queue()

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
    signin_username_entry.delete(0,END)
    signin_password_entry.delete(0,END)
    signin_forget_entry.delete(0,END)
    signin_status_button.grid_remove()
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
        print("registered customers")
    elif signin_confirm_result == 2:
        print("vip customers")
    elif signin_confirm_result == 3:
        print("delivery man")
    elif signin_confirm_result == 4:
        print("chef")
    elif signin_confirm_result == 5:
        print("manager")

def signin_forget_button_action():
    reset_gui()
    signin_forget_label.grid(row=0, column=0)
    signin_forget_entry.grid(row=0, column=1)
    signin_retrive_button.grid(row=1, column=1)
    signin_back_button.grid(row=1, column=0)
    window_center()

def signin_retrieve_button_action():
    signin_retrive_result = forget.retrieve(signin_forget_entry.get())
    messagebox.showinfo("",signin_retrive_result)

def signin_interface():
    reset_gui()
    signin_username_label.grid(row=0, column=0)
    signin_password_label.grid(row=1, column=0)
    signin_username_entry.grid(row=0, column=1)
    signin_password_entry.grid(row=1, column=1)
    signin_confirm_button.grid(row=2, column=1)
    signin_forget_button.grid(row=2, column=0)
    window_center()

def start_interface():
    reset_gui()
    signin_status_button.grid(row=0, column=2)
    dish_image1.grid(row=1, column=0)
    dish_name1.grid(row=2, column=0)
    dish_image2.grid(row=1, column=1)
    dish_name2.grid(row=2, column=1)
    dish_image3.grid(row=1, column=2)
    dish_name3.grid(row=2, column=2)
    dish_image4.grid(row=3, column=0)
    dish_name4.grid(row=4, column=0)
    dish_image5.grid(row=3, column=1)
    dish_name5.grid(row=4, column=1)
    dish_image6.grid(row=3, column=2)
    dish_name6.grid(row=4, column=2)
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

#forget interface
signin_forget_entry = Entry(program)
signin_forget_label = Label(program, text="Email")
signin_retrive_button = Button(text="Retrive", command=signin_retrieve_button_action)
signin_back_button = Button(text="Back", command=signin_interface)

#start interface
balance_label = Label(program, text="")
signin_status_button = Button(text="Sign In", command=signin_interface)
next_page_button = Button(text="Next", command=menu_next_page)
previous_page_button = Button(text="Previous", command=menu_previous_page)
etc_photo = PhotoImage(file="images/etc.gif")
dish_image1 = Label(image=None)
dish_name1 = Label(program, text="")
dish_image2 = Label(image=None)
dish_name2 = Label(program, text="")
dish_image3 = Label(image=None)
dish_name3 = Label(program, text="")
dish_image4 = Label(image=None)
dish_name4 = Label(program, text="")
dish_image5 = Label(image=None)
dish_name5 = Label(program, text="")
dish_image6 = Label(image=None)
dish_name6 = Label(program, text="")

def test():
    dish_image1.config(image=etc_photo)
    dish_image2.config(image=etc_photo)
    dish_image3.config(image=etc_photo)
    dish_image4.config(image=etc_photo)
    dish_image5.config(image=etc_photo)
    dish_image6.config(image=etc_photo)
    dish_name1.config(text="1")
    dish_name2.config(text="2")
    dish_name3.config(text="3")
    dish_name4.config(text="4")
    dish_name5.config(text="5")
    dish_name6.config(text="6")

start_interface()
test()
window_center()
program.mainloop()