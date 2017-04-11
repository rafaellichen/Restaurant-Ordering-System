from tkinter import *
from tkinter import messagebox
import time
import threading
import queue
import sys
from os import system

import signin
import bar
import element
import manage
import shop

program = Tk()
program.title("Restaurant Ordering System")
program.resizable(width=False, height=False)

menubar = Menu(program)
chef_list = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menus", menu=chef_list)
program.config(menu=menubar)

#variables
class user:
    def __init__(self):
        self.user_level = 0
        self.shopping_cart = []
        self.current_menu = []
        self.top_menu = []
        self.total = 0
        self.uid = -1

class parameter:
    def __init__(self):
        self.menu_max_page = 0
        self.menu_current_page = 1
        self.chef_list = []
        self.menu_list = []
        self.image_list = []
        self.name_list = []
        self.price_list = []
        self.current_chef_uid = -1
        self.current_chef_name = "All"

global current_parameter
global current_user
current_parameter = parameter()
current_user = user()

temp = bar.chef_in_list()
current_parameter.chef_list = temp
chef_list.delete(0,END)
chef_list.add_command(label="All", command=lambda: bar_change_menu("all","All"))
chef_list.add_command(label="Top", command=lambda: bar_change_menu("top","Top"))
for e,f in zip(temp[0],temp[1]):
    chef_list.add_command(label=str(e), command=lambda uid=f,name=e: bar_change_menu(uid,name))

def refresh_menu():
    if current_parameter.current_chef_uid != -1:
        bar_change_menu(current_parameter.current_chef_uid,current_parameter.current_chef_name)
    else:
        bar_change_menu("all",current_parameter.current_chef_name)

def bar_change_menu(uid,name):
    if uid == "all":
        current_parameter.current_chef_uid = uid
        current_parameter.current_chef_name = name
        chef_name.config(text=current_parameter.current_chef_name)
        start_interface()
    elif uid == "top":
        if current_user.uid == -1:
            messagebox.showinfo("", "Please log in first")
        else:
            current_parameter.current_chef_uid = uid
            current_parameter.current_chef_name = name
            chef_name.config(text=current_parameter.current_chef_name)
            top_menu_list(element.get_top_listing(current_user.uid))
    else:
        current_parameter.current_chef_uid = uid
        current_parameter.current_chef_name = name
        chef_name.config(text=current_parameter.current_chef_name)
        current_parameter.menu_list = bar.get_menu_list(uid)
        current_parameter.image_list = bar.get_image_list(uid)
        current_parameter.name_list = bar.get_name_list(uid)
        current_parameter.price_list = bar.get_price_list(uid)
    if (len(current_parameter.menu_list)-1) % 6 == 0:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6)
    else:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6 + 1)
    current_parameter.menu_current_page = 1
    page_change()
    display_menu()

def top_menu_list(did_list):
    if len(did_list) == 0:
        messagebox.showinfo("", "Please make some purchases first")
    else:
        current_parameter.menu_list = did_list
        current_parameter.image_list = bar.get_top_image_list(did_list)
        current_parameter.name_list = bar.get_top_name_list(did_list)
        current_parameter.price_list = bar.get_top_price_list(did_list)

def set_parameter():
    current_parameter.menu_list = element.get_menu_list()
    current_parameter.image_list = element.get_image_list()
    current_parameter.name_list = element.get_name_list()
    current_parameter.price_list = element.get_price_list()
    if (len(current_parameter.menu_list)-1) % 6 == 0:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6)
    else:
        current_parameter.menu_max_page = int((len(current_parameter.menu_list)-1)/6 + 1)
    current_parameter.menu_current_page = 1

def reset_gui():
    signin_username_entry.delete(0,END)
    signin_password_entry.delete(0,END)
    signin_forget_entry.delete(0,END)
    register_password_entry.delete(0,END)
    register_username_entry.delete(0,END)
    register_email_entry.delete(0,END)
    for widget in program.winfo_children():
        widget.grid_remove()

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
    signin_confirm_result = signin.validate(signin_username_entry.get(),
                                            signin_password_entry.get())
    # write function to change the software interface based on the type of user
    # replace print command
    if signin_confirm_result == 10:
        signin_username_entry.delete(0,END)
        signin_password_entry.delete(0,END)
    else:
        if signin_confirm_result == False:
            messagebox.showinfo("","Username or Password is incorrect")
            signin_username_entry.delete(0,END)
            signin_password_entry.delete(0,END)
        elif signin_confirm_result[0] == 1 or signin_confirm_result[0] == 2:
            current_user.uid = signin_confirm_result[1]
            current_user.user_level = signin_confirm_result[0]
            start_interface()
        elif signin_confirm_result[0] == 3:
            current_user.user_level = 3
            delivery_interface()
        elif signin_confirm_result[0] == 4:
            current_user.user_level = 4
            start_interface()
        elif signin_confirm_result[0] == 5:
            current_user.user_level = 5
            manager_interface()

def signin_forget_button_action():
    reset_gui()
    signin_forget_label.grid(row=0, column=0)
    signin_forget_entry.grid(row=0, column=1)
    signin_retrive_button.grid(row=1, column=1)
    forget_back_button.grid(row=1, column=0)
    window_center()

def signin_retrieve_button_action():
    messagebox.showinfo("",signin.retrieve(signin_forget_entry.get()))

def signout_button_action():
    current_user.user_level = 0
    start_interface()  

def signin_interface():
    reset_gui()
    signin_username_label.grid(row=0, column=0)
    signin_password_label.grid(row=1, column=0)
    signin_username_entry.grid(row=0, column=1)
    signin_password_entry.grid(row=1, column=1)
    signin_confirm_button.grid(row=2, column=1)
    signin_forget_button.grid(row=2, column=0)
    register_button.grid(row=3, column=1)
    signin_back_button.grid(row=3, column=0)
    window_center()

def register_button_action():
    reset_gui()
    register_username_entry.grid(row=0, column=1)
    register_username_label.grid(row=0, column=0)
    register_password_entry.grid(row=1, column=1)
    register_password_label.grid(row=1, column=0)
    register_email_entry.grid(row=2, column=1)
    register_email_label.grid(row=2, column=0)
    register_enter_button.grid(row=4, column=1)
    register_back_button.grid(row=4, column=0)

def become_member_button_action():
    result = messagebox.askyesno("", "Fixed amount of deposit ($50) is required. Still wish to apply?")
    if result:
        messagebox.showinfo("",signin.register(register_username_entry.get(),
                            register_password_entry.get(),
                            register_email_entry.get()))
        register_password_entry.delete(0,END)
        register_username_entry.delete(0,END)
        register_email_entry.delete(0,END)

def shopping_cart_buttom_action():
    reset_gui()
    shopping_sum_of_total= Label(program,text= current_user.total)
    shopping_total_label.grid(row=0,column=0)
    shopping_sum_of_total.grid(row=1,column=0)
    shopping_checkout_buttom.grid(row=2,column=0)
    signin_back_button.grid(row=3, column=0)
    window_center()

def add_car_buttom_action(i):
    reset_gui()
    shopping_image=dish_image_list[i]
    shopping_image.grid(row=0,column=0)
    shopping_name= dish_name_list[i]
    shopping_name.grid(row=1,column=0)
    shopping_price.append(current_parameter.price_list[i])
    dish_price_list[i].grid(row=2,column=0)
    shopping_did.append(dish_did_list[i])
    label_quantity_entry.grid(row=4,column=0)
    label_quantity.grid(row=3, column=0)
    signin_back_button.grid(row=6, column=0)
    shpping_enter_button.grid(row=5,column=0)
    window_center()

def shpping_enter_button_action():
    if shop.check_quantity(label_quantity_entry.get()):
        for i in range(int(label_quantity_entry.get())):
            current_user.shopping_cart.append(shopping_did[-1])
            current_user.total += int(shopping_price[-1])
    messagebox.showinfo("", "The item has been add on your shopping cart")
    label_quantity_entry.delete(0,END)

def page_change():
    if current_parameter.menu_current_page == 1:
        previous_page_button.config(state=DISABLED)
    else:
        previous_page_button.config(state=NORMAL)
    if current_parameter.menu_current_page == current_parameter.menu_max_page:
        next_page_button.config(state=DISABLED)
    else:
        next_page_button.config(state=NORMAL)
    dish_image1.config(image=etc_photo)
    dish_image2.config(image=etc_photo)
    dish_image3.config(image=etc_photo)
    dish_image4.config(image=etc_photo)
    dish_image5.config(image=etc_photo)
    dish_image6.config(image=etc_photo)
    dish_name1.config(text="Coming soon...")
    dish_name2.config(text="Coming soon...")
    dish_name3.config(text="Coming soon...")
    dish_name4.config(text="Coming soon...")
    dish_name5.config(text="Coming soon...")
    dish_name6.config(text="Coming soon...")
    dish_price1.config(text="")
    dish_price2.config(text="")
    dish_price3.config(text="")
    dish_price4.config(text="")
    dish_price5.config(text="")
    dish_price6.config(text="")

def display_menu():
    i=0
    while i<6:
        dish_did_list[i]=-1
        i+=1
    if current_parameter.menu_current_page != current_parameter.menu_max_page:
        for i in range(current_parameter.menu_current_page*6-6,current_parameter.menu_current_page*6):
            dish_did_list[i-(current_parameter.menu_current_page-1)*6] = current_parameter.menu_list[i]
            dish_name_list[i-(current_parameter.menu_current_page-1)*6].config(text=current_parameter.name_list[i])
            dish_price_list[i-(current_parameter.menu_current_page-1)*6].config(text=current_parameter.price_list[i])
            dish_img_list[i-(current_parameter.menu_current_page-1)*6] = PhotoImage(file=current_parameter.image_list[i])
            dish_image_list[i-(current_parameter.menu_current_page-1)*6].config(image=dish_img_list[i-(current_parameter.menu_current_page-1)*6])
    else:
        i=0
        for e in current_parameter.menu_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_did_list[i]=e
            i+=1
        i=0
        for e in current_parameter.image_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_img_list[i] = PhotoImage(file=e)
            dish_image_list[i].config(image=dish_img_list[i])
            i+=1
        i=0
        for e in current_parameter.name_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_name_list[i].config(text=e)
            i+=1
        i=0
        for e in current_parameter.price_list[(current_parameter.menu_current_page-1)*6:-1]:
            dish_price_list[i].config(text=e)
            i+=1
    if current_user.user_level != 0:
        i=0
        for e in dish_did_list:
            if e == -1:
                dish_buy_list[i].config(state=DISABLED)
            else:
                dish_buy_list[i].config(state=NORMAL)
            i+=1
    
def menu_next_page():
    current_parameter.menu_current_page += 1
    page_change()
    display_menu()

def menu_previous_page():
    current_parameter.menu_current_page -= 1
    page_change()
    display_menu()

def delivery_interface():
    reset_gui()
    node0.grid (row=0, column=0)
    node1.grid (row=0, column=2)
    node2.grid (row=0, column=4)
    node3.grid (row=0, column=6)
    node4.grid (row=0, column=8)
    node5.grid (row=2, column=0)    
    node6.grid (row=2, column=2)
    node7.grid (row=2, column=4)
    node8.grid (row=2, column=6)
    node9.grid (row=2, column=8)
    node10.grid (row=4, column=0)
    node11.grid (row=4, column=2)
    node12.grid (row=4, column=4)
    node13.grid (row=4, column=6)
    node14.grid (row=4, column=8)
    node15.grid (row=6, column=0)
    node16.grid (row=6, column=2)
    node17.grid (row=6, column=4)
    node18.grid (row=6, column=6)
    node19.grid (row=6, column=8)
    node20.grid (row=8, column=0)
    node21.grid (row=8, column=2)
    node22.grid (row=8, column=4)
    node23.grid (row=8, column=6)
    node24.grid (row=8, column=8)
    edge1.grid(row=0, column=1)
    edge2.grid(row=0, column=3)
    edge3.grid(row=0, column=5)
    edge4.grid(row=0, column=7)
    edge5.grid(row=1, column=0)
    edge6.grid(row=1, column=2)
    edge7.grid(row=1, column=4)
    edge8.grid(row=1, column=6)
    edge9.grid(row=1, column=8)
    edge10.grid(row=2, column=1)
    edge11.grid(row=2, column=3)
    edge12.grid(row=2, column=5)
    edge13.grid(row=2, column=7)
    edge14.grid(row=3, column=0)
    edge15.grid(row=3, column=2)
    edge16.grid(row=3, column=4)
    edge17.grid(row=3, column=6)
    edge18.grid(row=3, column=8)
    edge19.grid(row=4, column=1)
    edge20.grid(row=4, column=3)
    edge21.grid(row=4, column=5)
    edge22.grid(row=4, column=7)
    edge23.grid(row=5, column=0)
    edge24.grid(row=5, column=2)
    edge25.grid(row=5, column=4)
    edge26.grid(row=5, column=6)
    edge27.grid(row=5, column=8)
    edge28.grid(row=6, column=1)
    edge29.grid(row=6, column=3)
    edge30.grid(row=6, column=5)
    edge31.grid(row=6, column=7)
    edge32.grid(row=7, column=0)
    edge33.grid(row=7, column=2)
    edge34.grid(row=7, column=4)
    edge35.grid(row=7, column=6)
    edge36.grid(row=7, column=8)
    edge37.grid(row=8, column=1)
    edge38.grid(row=8, column=3)
    edge39.grid(row=8, column=5)
    edge40.grid(row=8, column=7)

def start_interface():
    reset_gui()
    if current_user.user_level == 0:
        dish_buy1.config(state=DISABLED)
        dish_buy2.config(state=DISABLED)
        dish_buy3.config(state=DISABLED)
        dish_buy4.config(state=DISABLED)
        dish_buy5.config(state=DISABLED)
        dish_buy6.config(state=DISABLED)
    else:
        dish_buy1.config(state=NORMAL)
        dish_buy2.config(state=NORMAL)
        dish_buy3.config(state=NORMAL)
        dish_buy4.config(state=NORMAL)
        dish_buy5.config(state=NORMAL)
        dish_buy6.config(state=NORMAL)
    chef_name.config(text="All")
    current_parameter.current_chef_name = "All"
    current_parameter.current_chef_uid = -1
    set_parameter()
    page_change()
    display_menu()
    refresh_button.grid(row=0, column=0)
    chef_name.grid(row=1, column=1)
    if(current_user.user_level == 0):
        signin_button.grid(row=0, column=2)
    else:
        info_button.grid(row=0, column=2)
        signout_button.grid(row=1, column=2)
    shopping_cart_items.grid(row=0, column=1)
    dish_image1.grid(row=2, column=0)
    dish_name1.grid(row=3, column=0)
    dish_price1.grid(row=4, column=0)
    dish_buy1.grid(row=5, column=0)
    dish_image2.grid(row=2, column=1)
    dish_name2.grid(row=3, column=1)
    dish_price2.grid(row=4, column=1)
    dish_buy2.grid(row=5, column=1)
    dish_image3.grid(row=2, column=2)
    dish_name3.grid(row=3, column=2)
    dish_price3.grid(row=4, column=2)
    dish_buy3.grid(row=5, column=2)
    dish_image4.grid(row=6, column=0)
    dish_name4.grid(row=7, column=0)
    dish_price4.grid(row=8, column=0)
    dish_buy4.grid(row=9, column=0)
    dish_image5.grid(row=6, column=1)
    dish_name5.grid(row=7, column=1)
    dish_price5.grid(row=8, column=1)
    dish_buy5.grid(row=9, column=1)
    dish_image6.grid(row=6, column=2)
    dish_name6.grid(row=7, column=2)
    dish_price6.grid(row=8, column=2)
    dish_buy6.grid(row=9, column=2)
    next_page_button.grid(row=10, column=2)
    previous_page_button.grid(row=10, column=0)
    window_center()

def manager_interface():
    reset_gui()
    signout_button.grid(row=0, column=2)
    users_approve_list_label.grid(row=1, column=0)
    update_all_button.grid(row=0, column=0)
    users_approve_list.grid(row=2, column=0)
    user_approved_list_label.grid(row=1, column=1)
    user_approved_list.grid(row=2, column=1)
    user_declined_list_label.grid(row=1, column=2)
    user_declined_list.grid(row=2, column=2)
    dish_compliments_list_label.grid(row=3, column=0)
    dish_compliments_list.grid(row=4, column=0)
    dish_approved_compliements_list_label.grid(row=3, column=1)
    dish_approved_compliements_list.grid(row=4, column=1)
    dish_declined_compliments_list_label.grid(row=3, column=2)
    dish_declined_compliments_list.grid(row=4, column=2)
    dish_complaints_list_label.grid(row=5, column=0)
    dish_complaints_list.grid(row=6, column=0)
    dish_approved_compliants_list_label.grid(row=5, column=1)
    dish_approved_compliants_list.grid(row=6, column=1)
    dish_declined_compliants_list.grid(row=6, column=2)
    dish_declined_compliants_list_label.grid(row=5, column=2)
    manager_approve_button.grid(row=9, column=2)
    manager_decline_button.grid(row=9, column=0)
    manager_update_all_action()
    window_center()

def manager_update_all_action():
    dish_compliments_list.delete(0,END)
    dish_complaints_list.delete(0,END)
    users_approve_list.delete(0,END)
    user_approved_list.delete(0,END)
    user_declined_list.delete(0,END)
    dish_approved_compliements_list.delete(0, END)
    dish_declined_compliments_list.delete(0, END)
    dish_approved_compliants_list.delete(0, END)
    dish_declined_compliants_list.delete(0, END)
    pending_list = element.get_pending_registrations()
    compliments_list = element.get_pending_compliments()
    complaints_list = element.get_pending_complaints()
    approved_list = element.get_users(1)
    declined_list = element.get_users(-1)
    blocked_list = element.get_users(0)
    approved_compliments_list = element.get_comment(1,1)
    declined_compliments_list = element.get_comment(1,-1)
    approved_compliants_list = element.get_comment(0,1)
    declined_compliants_list = element.get_comment(0,-1)
    for item in approved_compliments_list:
        dish_approved_compliements_list.insert(END, item)
    for item in declined_compliments_list:
        dish_declined_compliments_list.insert(END, item)
    for item in approved_compliants_list:
        dish_approved_compliants_list.insert(END, item)
    for item in declined_compliants_list:
        dish_declined_compliants_list.insert(END, item)
    for item in pending_list:
        users_approve_list.insert(END, item)
    for item in compliments_list:
        dish_compliments_list.insert(END, item)
    for item in complaints_list:
        dish_complaints_list.insert(END, item)
    for item in approved_list:
        user_approved_list.insert(END, item)
    for item in declined_list:
        user_declined_list.insert(END, item)
    
def manager_approve_decline_button_action(input):
    try:
        manage.approve_pending_registrations(users_approve_list.get(users_approve_list.curselection()), input)
        manager_update_all_action()
    except TclError:
        try:
            manage.approve_compliments(dish_compliments_list.get(dish_compliments_list.curselection()), input)
            manager_update_all_action()
        except TclError:
            try:
                manage.approve_complaints(dish_complaints_list.get(dish_complaints_list.curselection()), input)
                manager_update_all_action()
            except TclError:
                try:
                    manage.approve_pending_registrations(user_approved_list.get(user_approved_list.curselection()), input)
                    manager_update_all_action()
                except TclError:
                    try:
                        manage.approve_pending_registrations(user_declined_list.get(user_declined_list.curselection()), input)
                        manager_update_all_action()
                    except TclError:
                        try:
                            manage.approve_compliments(dish_approved_compliements_list.get(dish_approved_compliements_list.curselection()), input)
                            manager_update_all_action()
                        except TclError:
                            try:
                                manage.approve_compliments(dish_declined_compliments_list.get(dish_declined_compliments_list.curselection()), input)
                                manager_update_all_action()
                            except TclError:
                                try:
                                    manage.approve_complaints(dish_approved_compliants_list.get(dish_approved_compliants_list.curselection()), input)
                                    manager_update_all_action()
                                except TclError:
                                    try:
                                        manage.approve_complaints(dish_declined_compliants_list.get(dish_declined_compliants_list.curselection()), input)
                                        manager_update_all_action()
                                    except TclError:
                                        messagebox.showinfo("","Please select an item to process")

#manager interface
users_approve_list = Listbox(program)
users_approve_list_label = Label(program, text="Pending registrations")
manager_approve_button = Button(text="Approve", command=lambda: manager_approve_decline_button_action(1))
manager_decline_button = Button(text="Decline", command=lambda: manager_approve_decline_button_action(-1))
dish_compliments_list_label = Label(program, text="Pending compliments")
dish_compliments_list = Listbox(program)
dish_complaints_list_label = Label(program, text="Pending complaints")
dish_complaints_list = Listbox(program)
update_all_button = Button(text="Refresh", command=manager_update_all_action)
dish_approved_compliements_list_label = Label(program, text="Approved compliments")
dish_approved_compliants_list_label = Label(program, text="Approved complaints")
dish_declined_compliments_list_label = Label(program, text="Declined compliments")
dish_declined_compliants_list_label = Label(program, text="Declined compliants")
user_approved_list_label = Label(program, text="Approved users")
user_declined_list_label = Label(program, text="Declined users")
dish_approved_compliements_list = Listbox(program)
dish_approved_compliants_list = Listbox(program)
dish_declined_compliments_list = Listbox(program)
dish_declined_compliants_list = Listbox(program)
user_approved_list = Listbox(program)
user_declined_list = Listbox(program)

#signin interface
signin_username_label = Label(program, text="Username")
signin_password_label = Label(program, text="Password")
signin_username_entry = Entry(program)
signin_password_entry = Entry(program)
signin_confirm_button = Button(text="Sign in", command=signin_confirm_button_action)
signin_forget_button = Button(text="Forget", command=signin_forget_button_action)
signin_back_button = Button(text="Back", command=start_interface)
register_button = Button(text="Register", command=register_button_action)

#forget interface
signin_forget_entry = Entry(program)
signin_forget_label = Label(program, text="Email")
signin_retrive_button = Button(text="Retrive", command=signin_retrieve_button_action)
forget_back_button = Button(text="Back", command=signin_interface)

#register_interface
register_username_entry = Entry(program)
register_username_label = Label(program, text="Username")
register_password_entry = Entry(program)
register_password_label = Label(program, text="Password")
register_email_entry = Entry(program)
register_email_label = Label(program, text="Email")
register_enter_button = Button(text="Become Member", command=become_member_button_action)
register_back_button = Button(text="Back", command=signin_interface)

#shpping cart interface
label_quantity_entry = Entry(program)
label_quantity = Label(program, text="Please enter item quantities")
shpping_enter_button = Button(text="Enter", command=shpping_enter_button_action)
purchased_item_quantity_label=Label(program,text = "You have been add item on your shpping car")
shopping_image = Label(image=None)
shopping_did = []
shopping_name=[]
shopping_price=[]
shopping_quantity=[]
shopping_checkout_buttom=Button(text= "Check out",command= None)
shopping_total_label = Label(program,text="Total:")

#delivery interface
node_matrix = [[0 for i in range(25)] for j in range(25)]
edge_matrix = [[0 for i in range(25)] for j in range(25)]
for i in range(0,25):
    for j in range(0,25):
        node_matrix[i][j] = -1
for i in range(0,25):
    for j in range(0,25):
        edge_matrix[i][j] = 0
node_matrix[0][0] = 1
node_matrix[0][1] = 1
node_matrix[0][5] = 1
node_matrix[1][0] = 1
node_matrix[1][1] = 1
node_matrix[1][2] = 1
node_matrix[1][6] = 1
node_matrix[2][1] = 1
node_matrix[2][2] = 1
node_matrix[2][3] = 1
node_matrix[2][7] = 1
node_matrix[3][2] = 1
node_matrix[3][3] = 1
node_matrix[3][4] = 1
node_matrix[3][8] = 1
node_matrix[4][3] = 1
node_matrix[4][4] = 1
node_matrix[4][9] = 1
node_matrix[5][0] = 1
node_matrix[5][5] = 1
node_matrix[5][6] = 1
node_matrix[5][10] = 1
node_matrix[6][1] = 1
node_matrix[6][5] = 1
node_matrix[6][6] = 1
node_matrix[6][7] = 1
node_matrix[6][11] = 1
node_matrix[7][2] = 1
node_matrix[7][6] = 1
node_matrix[7][7] = 1
node_matrix[7][8] = 1
node_matrix[7][12] = 1
node_matrix[8][3] = 1
node_matrix[8][7] = 1
node_matrix[8][8] = 1
node_matrix[8][9] = 1
node_matrix[8][13] = 1
node_matrix[9][4] = 1
node_matrix[9][8] = 1
node_matrix[9][9] = 1
node_matrix[9][14] = 1
node_matrix[10][5] = 1
node_matrix[10][10] = 1
node_matrix[10][11] = 1
node_matrix[10][15] = 1
node_matrix[11][6] = 1
node_matrix[11][10] = 1
node_matrix[11][11] = 1
node_matrix[11][12] = 1
node_matrix[11][16] = 1
node_matrix[12][7] = 1
node_matrix[12][11] = 1
node_matrix[12][12] = 1
node_matrix[12][13] = 1
node_matrix[12][17] = 1
node_matrix[13][8] = 1
node_matrix[13][12] = 1
node_matrix[13][13] = 1
node_matrix[13][14] = 1
node_matrix[13][18] = 1
node_matrix[14][9] = 1
node_matrix[14][13] = 1
node_matrix[14][14] = 1
node_matrix[14][19] = 1
node_matrix[15][15] = 1
node_matrix[15][16] = 1
node_matrix[15][20] = 1
node_matrix[15][10] = 1
node_matrix[16][15] = 1
node_matrix[16][16] = 1
node_matrix[16][14] = 1
node_matrix[16][17] = 1
node_matrix[16][21] = 1
node_matrix[17][16] = 1
node_matrix[17][17] = 1
node_matrix[17][12] = 1
node_matrix[17][18] = 1
node_matrix[17][22] = 1
node_matrix[18][17] = 1
node_matrix[18][18] = 1
node_matrix[18][13] = 1
node_matrix[18][19] = 1
node_matrix[18][23] = 1
node_matrix[19][14] = 1
node_matrix[19][19] = 1
node_matrix[19][18] = 1
node_matrix[19][24] = 1
node_matrix[20][15] = 1
node_matrix[20][20] = 1
node_matrix[20][21] = 1
node_matrix[21][16] = 1
node_matrix[21][21] = 1
node_matrix[21][20] = 1
node_matrix[21][22] = 1
node_matrix[22][17] = 1
node_matrix[22][22] = 1
node_matrix[22][21] = 1
node_matrix[22][23] = 1
node_matrix[23][18] = 1
node_matrix[23][23] = 1
node_matrix[23][22] = 1
node_matrix[23][24] = 1
node_matrix[24][19] = 1
node_matrix[24][24] = 1
node_matrix[24][23] = 1
edge1 = edge_matrix[0][1]
edge2 = edge_matrix[1][2]
edge3 = edge_matrix[2][3]
edge4 = edge_matrix[3][4]
edge5 = edge_matrix[0][5]
edge6 = edge_matrix[1][6]
edge7 = edge_matrix[2][7]
edge8 = edge_matrix[3][8]
edge9 = edge_matrix[4][9]
edge10 = edge_matrix[5][6]
edge11 = edge_matrix[6][7]
edge12 = edge_matrix[7][8]
edge13 = edge_matrix[8][9]
edge14 = edge_matrix[5][10]
edge15 = edge_matrix[6][11]
edge16 = edge_matrix[7][12]
edge17 = edge_matrix[8][13]
edge18 = edge_matrix[9][14]
edge19 = edge_matrix[10][11]
edge20 = edge_matrix[11][12]
edge21 = edge_matrix[12][13]
edge22 = edge_matrix[13][14]
edge23 = edge_matrix[10][15]
edge24 = edge_matrix[11][16]
edge25 = edge_matrix[12][17]
edge26 = edge_matrix[13][18]
edge27 = edge_matrix[14][19]
edge28 = edge_matrix[15][16]
edge29 = edge_matrix[16][17]
edge30 = edge_matrix[17][18]
edge31 = edge_matrix[18][19]
edge32 = edge_matrix[15][20]
edge33 = edge_matrix[16][21]
edge34 = edge_matrix[17][22]
edge35 = edge_matrix[18][23]
edge36 = edge_matrix[19][24]
edge37 = edge_matrix[20][21]
edge38 = edge_matrix[21][22]
edge39 = edge_matrix[22][23]
edge40 = edge_matrix[23][24]
node0 = Button(state=DISABLED)
node1 = Button(state=DISABLED)
node2 = Button(state=DISABLED)
node3 = Button(state=DISABLED)
node4 = Button(state=DISABLED)
node5 = Button(state=DISABLED)
node6 = Button(state=DISABLED)
node7 = Button(state=DISABLED)
node8 = Button(state=DISABLED)
node9 = Button(state=DISABLED)
node10 = Button(state=DISABLED)
node11 = Button(state=DISABLED)
node12 = Button(state=DISABLED)
node13 = Button(state=DISABLED)
node14 = Button(state=DISABLED)
node15 = Button(state=DISABLED)
node16 = Button(state=DISABLED)
node17 = Button(state=DISABLED)
node18 = Button(state=DISABLED)
node19 = Button(state=DISABLED)
node20 = Button(state=DISABLED)
node21 = Button(state=DISABLED)
node22 = Button(state=DISABLED)
node23 = Button(state=DISABLED)
node24 = Button(state=DISABLED)
edge1 = Label(text="__")
edge2 = Label(text="__")
edge3 = Label(text="__")
edge4 = Label(text="__")
edge5 = Label(text="|")
edge6 = Label(text="|")
edge7 = Label(text="|")
edge8 = Label(text="|")
edge9 = Label(text="|")
edge10 = Label(text="__")
edge11= Label(text="__")
edge12 = Label(text="__")
edge13 = Label(text="__")
edge14 = Label(text="|")
edge15 = Label(text="|")
edge16 = Label(text="|")
edge17 = Label(text="|")
edge18 = Label(text="|")
edge19 = Label(text="__")
edge20 = Label(text="__")
edge21 = Label(text="__")
edge22 = Label(text="__")
edge23 = Label(text="|")
edge24 = Label(text="|")
edge25 = Label(text="|")
edge26 = Label(text="|")
edge27 = Label(text="|")
edge28 = Label(text="__")
edge29 = Label(text="__")
edge30 = Label(text="__")
edge31 = Label(text="__")
edge32 = Label(text="|")
edge33 = Label(text="|")
edge34 = Label(text="|")
edge35 = Label(text="|")
edge36 = Label(text="|")
edge37 = Label(text="__")
edge38 = Label(text="__")
edge39 = Label(text="__")
edge40 = Label(text="__")

#start interface
chef_name = Label(program, text="All")
info_button = Button(text="Profile", command=None)
refresh_button = Button(text="Refresh", command=refresh_menu)
shopping_cart_items = Button(text="Your Shopping Cart", command=shopping_cart_buttom_action)
signout_button = Button(text="Sign Out", command=signout_button_action)
signin_button = Button(text="Sign In", command=signin_interface)
next_page_button = Button(text="Next", command=menu_next_page)
previous_page_button = Button(text="Previous", command=menu_previous_page)
etc_photo = PhotoImage(file="images/etc.gif")
dish_image1 = Label(image=None)
dish_name1 = Label(program, text="Name")
dish_price1 = Label(program, text="Price")
dish_buy1 = Button(text="Add to cart", command=lambda: add_car_buttom_action(0))
dish_did1=""
dish_image2 = Label(image=None)
dish_name2 = Label(program, text="Name")
dish_price2 = Label(program, text="Price")
dish_buy2 = Button(text="Add to cart", command=lambda: add_car_buttom_action(1))
dish_did2=""
dish_image3 = Label(image=None)
dish_name3 = Label(program, text="Name")
dish_price3 = Label(program, text="Price")
dish_buy3 = Button(text="Add to cart", command=lambda: add_car_buttom_action(2))
dish_did3=""
dish_image4 = Label(image=None)
dish_name4 = Label(program, text="Name")
dish_price4 = Label(program, text="Price")
dish_buy4 = Button(text="Add to cart", command=lambda: add_car_buttom_action(3))
dish_did4=""
dish_image5 = Label(image=None)
dish_name5 = Label(program, text="Name")
dish_price5 = Label(program, text="Price")
dish_buy5 = Button(text="Add to cart", command=lambda: add_car_buttom_action(4))
dish_did5=""
dish_image6 = Label(image=None)
dish_name6 = Label(program, text="Name")
dish_price6 = Label(program, text="Price")
dish_buy6 = Button(text="Add to cart", command=lambda: add_car_buttom_action(5))
dish_did6=""
img1=""
img2=""
img3=""
img4=""
img5=""
img6=""

dish_image_list = [dish_image1, dish_image2, dish_image3, dish_image4, dish_image5, dish_image6]
dish_buy_list = [dish_buy1, dish_buy2, dish_buy3, dish_buy4, dish_buy5, dish_buy6]
dish_did_list = [dish_did1, dish_did2, dish_did3, dish_did4, dish_did5, dish_did6]
dish_name_list = [dish_name1, dish_name2, dish_name3, dish_name4, dish_name5, dish_name6]
dish_price_list = [dish_price1, dish_price2, dish_price3, dish_price4, dish_price5, dish_price6]
dish_img_list = [img1, img2, img3, img4, img5, img6]

start_interface()
window_center()
program.mainloop()