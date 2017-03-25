from tkinter import *
from tkinter import messagebox
import time
import threading
import queue
import sys

import signin
import forget

program = Tk()
program.title("Restaurant Ordering System")
program.resizable(width=False, height=False)

#constants
user_level = 0

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


window_center()
program.mainloop()