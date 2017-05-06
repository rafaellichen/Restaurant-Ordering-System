from tkinter import *
from tkinter import messagebox

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
        self.menu_max_page = 1
        self.menu_current_page = 1
        self.chef_list = []
        self.menu_list = []
        self.image_list = []
        self.name_list = []
        self.price_list = []
        self.current_chef_uid = -1
        self.current_chef_name = "All"
        self.employee_type = 0
        self.current_cart_page = 1
        self.max_cart_page = 1
        self.shopping_did_list = []
        self.shopping_quantity_list = []
        self.shopping_name_list = []
        self.shopping_price_list = []
        self.shopping_image_list = []
        self.available_dish = []
        self.added_dish = []
        self.star_food_rate = 0
        self.star_delivery_rate = 0
        self.alldish = []

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

def comment_interface():
    reset_gui()
    order_history_label.grid(row=0, column=0)
    combined_rate_frame.grid(row=0, column=1, rowspan=2)
    rate_order_list.grid(row=1, column=0)
    refresh_comment()

def refresh_comment():
    for e in star_food_list:
        e.config(image=star_b)
    for e in star_delivery_list:
        e.config(image=star_b)
    rate_order_list.delete(0,END)
    for e in element.get_ddid_list(current_user.uid):
        rate_order_list.insert(END, e)
    current_parameter.star_food_rate = 0
    current_parameter.star_delivery_rate = 0
    rate_comment.delete(0,END)

def submit_rating():
    if current_parameter.star_food_rate == 0 or current_parameter.star_delivery_rate == 0:
        messagebox.showwarning("","Please rate food and delivery from 1 star to 5 stars")
    else:
        result = messagebox.askyesno("", "Food: "+str(current_parameter.star_food_rate)+"\nDelivery: "
                                    +str(current_parameter.star_delivery_rate)+"\nComment: "+str(rate_comment.get())+
                                    "\nConfirm?")
        if result:
            try:
                order_did = element.get_did_list(rate_order_list.get(rate_order_list.curselection()))
                element.save_comment(current_parameter.star_delivery_rate, current_parameter.star_food_rate,
                                     current_user.uid, order_did, rate_comment.get())
                element.save_rating(current_parameter.star_food_rate, order_did, current_user.user_level)
                element.delivery_rating(current_parameter.star_delivery_rate, rate_order_list.get(rate_order_list.curselection()))
                refresh_comment()
            except TclError:
                messagebox.showwarning("", "Please select an order to rate")

def star_food_change(num):
    for e in star_food_list:
        e.config(image=star_b)
    i=0
    while i<num:
        star_food_list[i].config(image=star_c)
        i+=1
    current_parameter.star_food_rate = num

def star_delivery_change(num):
    for e in star_delivery_list:
        e.config(image=star_b)
    i=0
    while i<num:
        star_delivery_list[i].config(image=star_c)
        i+=1
    current_parameter.star_delivery_rate = num

def refresh_menu():
    temp = bar.chef_in_list()
    current_parameter.chef_list = temp
    chef_list.delete(0,END)
    chef_list.add_command(label="All", command=lambda: bar_change_menu("all","All"))
    chef_list.add_command(label="Top", command=lambda: bar_change_menu("top","Top"))
    for e,f in zip(temp[0],temp[1]):
        chef_list.add_command(label=str(e), command=lambda uid=f,name=e: bar_change_menu(uid,name))
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
            messagebox.showwarning("", "Please log in first")
        else:
            current_parameter.current_chef_uid = uid
            current_parameter.current_chef_name = name
            chef_name.config(text=current_parameter.current_chef_name)
            top_menu_list(element.get_top_listing(current_user.uid))
    elif element.menu_check(uid):
        messagebox.showwarning("", "This chef has not yet added any dishes to the menu")
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
        messagebox.showwarning("", "Please make some purchases first")
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
    profile_deposit.delete(0,END)
    search_entry.delete(0,END)
    signin_username_entry.delete(0,END)
    signin_password_entry.delete(0,END)
    signin_forget_entry.delete(0,END)
    register_password_entry.delete(0,END)
    register_username_entry.delete(0,END)
    register_email_entry.delete(0,END)
    label_quantity_entry.delete(0,END)
    rate_order_list.delete(0,END)
    dish_name_entry.delete(0,END)
    price_entry.delete(0,END)
    description_entry.delete(0,END)
    image_entry.delete(0,END)
    for widget in program.winfo_children():
        widget.grid_remove()

def signin_confirm_button_action():
    signin_confirm_result = signin.validate(signin_username_entry.get(),
                                            signin_password_entry.get())
    if signin_confirm_result == 10:
        signin_username_entry.delete(0,END)
        signin_password_entry.delete(0,END)
    else:
        if signin_confirm_result == False:
            messagebox.showwarning("","Username or Password is incorrect")
            signin_username_entry.delete(0,END)
            signin_password_entry.delete(0,END)
        elif signin_confirm_result[0] == 1 or signin_confirm_result[0] == 2:
            current_user.uid = signin_confirm_result[1]
            current_user.user_level = signin_confirm_result[0]
            current_user.shopping_cart = shop.get_cart(current_user.uid)
            update_total()
            start_interface()
        elif signin_confirm_result[0] == 3:
            current_user.user_level = 3
            delivery_interface()
        elif signin_confirm_result[0] == 4:
            current_user.user_level = 4
            current_user.uid = signin_confirm_result[1]
            chef_interface()
        elif signin_confirm_result[0] == 5:
            current_user.user_level = 5
            manager_interface()

def chef_interface():
    reset_gui()
    available_dish_list.grid(row=2, column=0)
    available_dish_list.delete(0,END)
    add_new_dish_button.grid(row=0, column=0)
    signout_button.grid(row=0, column=2)
    current_dish_list.grid(row=2, column=2)
    current_dish_list.delete(0,END)
    available_dish_label.grid(row=1, column=0)
    current_dish_label.grid(row=1, column=2)
    chef_frame.grid(row=2, column=1)
    save_menu_button.grid(row=3, column=2)
    element.get_edit_menu(current_user.uid)
    temp_list = element.get_edit_menu(current_user.uid)
    current_parameter.available_dish = temp_list[0]
    current_parameter.added_dish = temp_list[1]
    for e in current_parameter.available_dish:
        available_dish_list.insert(END, e)
    for e in current_parameter.added_dish:
         if e != -1:
            current_dish_list.insert(END, e)

def add_new_dish_interface():
    reset_gui()
    add_back_button.grid(row=0, column=1)
    dish_name_label.grid(row=1, column=0)
    price_label.grid(row=2, column=0)
    description_label.grid(row=3, column=0)
    image_label.grid(row=4, column=0)
    save_button.grid(row=5, column=1)
    dish_name_entry.grid(row=1, column=1)
    price_entry.grid(row=2, column=1)
    description_entry.grid(row=3, column=1)
    image_entry.grid(row=4, column=1)



def update_edit_menu():
    available_dish_list.delete(0,END)
    current_dish_list.delete(0,END)
    for e in current_parameter.available_dish:
        available_dish_list.insert(END, e)
    for e in current_parameter.added_dish:
        if e != -1:
            current_dish_list.insert(END, e)

def save_menu_action():
    element.save_edit_menu(current_parameter.added_dish, current_user.uid)

def add_dish():
    try:
        item = available_dish_list.get(available_dish_list.curselection())
        current_parameter.available_dish.remove(int(item))
        current_parameter.added_dish.append(int(item))
    except TclError:
        messagebox.showwarning("", "Select an available dish to add")
    update_edit_menu()

def remove_dish():
    try:
        item = current_dish_list.get(current_dish_list.curselection())
        current_parameter.added_dish.remove(int(item))
        current_parameter.available_dish.append(int(item))
    except TclError:
        messagebox.showwarning("", "Select a current dish to remove")
    update_edit_menu()

def signin_forget_button_action():
    reset_gui()
    signin_forget_label.grid(row=0, column=0)
    signin_forget_entry.grid(row=0, column=1)
    signin_retrive_button.grid(row=1, column=1)
    forget_back_button.grid(row=1, column=0)

def signin_retrieve_button_action():
    messagebox.showinfo("",signin.retrieve(signin_forget_entry.get()))

def signout_button_action():
    current_user.user_level = 0
    current_user.uid = -1
    current_user.shopping_cart = []
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

def display_cart():
    i=0
    while i<6:
        cart_did_list[i]=-1
        i+=1
    if current_parameter.current_cart_page != current_parameter.max_cart_page:
        for i in range(current_parameter.current_cart_page*6-6,current_parameter.current_cart_page*6):
            cart_did_list[i-(current_parameter.current_cart_page-1)*6] = current_parameter.shopping_did_list[i]
            shopping_name_label_list[i-(current_parameter.current_cart_page-1)*6].config(text=current_parameter.shopping_name_list[i])
            cart_item_price_list[i-(current_parameter.current_cart_page-1)*6].config(text=current_parameter.shopping_price_list[i])
            cart_image_list[i-(current_parameter.current_cart_page-1)*6] = PhotoImage(file=current_parameter.shopping_image_list[i]).subsample(2,2)
            cart_item_image_list[i-(current_parameter.current_cart_page-1)*6].config(image=cart_image_list[i-(current_parameter.current_cart_page-1)*6])
            cart_item_entry_list[i-(current_parameter.current_cart_page-1)*6].config(state=NORMAL)
            cart_item_entry_list[i-(current_parameter.current_cart_page-1)*6].insert(0,current_parameter.shopping_quantity_list[i])
    else:
        i=0
        for e in current_parameter.shopping_did_list[(current_parameter.current_cart_page-1)*6:]:
            cart_did_list[i]=e
            i+=1
        i=0
        for e in current_parameter.shopping_image_list[(current_parameter.current_cart_page-1)*6:]:
            cart_image_list[i] = PhotoImage(file=e).subsample(2,2)
            cart_item_image_list[i].config(image=cart_image_list[i])
            i+=1
        i=0
        for e in current_parameter.shopping_name_list[(current_parameter.current_cart_page-1)*6:]:
            shopping_name_label_list[i].config(text=e)
            i+=1
        i=0
        for e in current_parameter.shopping_price_list[(current_parameter.current_cart_page-1)*6:]:
            cart_item_price_list[i].config(text=e)
            i+=1
        i=0
        for e in current_parameter.shopping_quantity_list[(current_parameter.current_cart_page-1)*6:]:
            cart_item_entry_list[i].config(state=NORMAL)
            cart_item_entry_list[i].insert(0,e)
            i+=1

def shoppingcart_checkout_button_action():
    if current_user.total == 0:
        messagebox.showwarning("", "Empty cart")
    else:
        result = shop.checkout_balance(current_user.user_level, current_user.total, current_user.uid)
        if current_user.user_level != 0 and result:
            shop.write_order(current_user.uid,current_user.shopping_cart)
            current_user.shopping_cart = []
            current_user.total = 0
            shopping_cart_button_action()
        manage.auto_vip_block()

def cart_page_change():
    if current_parameter.current_cart_page == 1:
        cart_previous.config(state=DISABLED)
    else:
        cart_previous.config(state=NORMAL)
    if current_parameter.current_cart_page == current_parameter.max_cart_page:
        cart_next.config(state=DISABLED)
    else:
        cart_next.config(state=NORMAL)
    cart_item_price1.config(text="--")
    cart_item_price2.config(text="--")
    cart_item_price3.config(text="--")
    cart_item_price4.config(text="--")
    cart_item_price5.config(text="--")
    cart_item_price6.config(text="--")
    shopping_name_label1.config(text="--")
    shopping_name_label2.config(text="--")
    shopping_name_label3.config(text="--")
    shopping_name_label4.config(text="--")
    shopping_name_label5.config(text="--")
    shopping_name_label6.config(text="--")
    for e in cart_item_entry_list:
        e.delete(0,END)
    cart_item1_entry.config(state=DISABLED)
    cart_item2_entry.config(state=DISABLED)
    cart_item3_entry.config(state=DISABLED)
    cart_item4_entry.config(state=DISABLED)
    cart_item5_entry.config(state=DISABLED)
    cart_item6_entry.config(state=DISABLED)
    cart_item1_image.config(image=etc_photo_small)
    cart_item2_image.config(image=etc_photo_small)
    cart_item3_image.config(image=etc_photo_small)
    cart_item4_image.config(image=etc_photo_small)
    cart_item5_image.config(image=etc_photo_small)
    cart_item6_image.config(image=etc_photo_small)

def set_cart_data():
    did_quantity = shop.get_list(current_user.shopping_cart)
    current_parameter.shopping_did_list = []
    current_parameter.shopping_quantity_list = []
    current_parameter.shopping_name_list = []
    current_parameter.shopping_price_list = []
    current_parameter.shopping_image_list = []
    for e in did_quantity:
        current_parameter.shopping_did_list.append(e[0])
        current_parameter.shopping_quantity_list.append(e[1])
    temp = shop.name_list(current_parameter.shopping_did_list)
    current_parameter.shopping_name_list = temp[0]
    current_parameter.shopping_price_list = temp[1]
    current_parameter.shopping_image_list = temp[2]
    if (len(current_parameter.shopping_did_list)) % 6 == 0 and len(current_parameter.shopping_did_list) != 0:
        current_parameter.max_cart_page = int((len(current_parameter.shopping_did_list))/6)
    else:
        current_parameter.max_cart_page = int((len(current_parameter.shopping_did_list))/6 + 1)
    current_parameter.current_cart_page = 1

def shopping_cart_button_action():
    reset_gui()
    set_cart_data()
    cart_page_change()
    display_cart()
    label_shoppingcart_item.grid(row=0,column=0)
    label_shoppingcart_price.grid(row=0,column=1)
    label_shoppingcart_quantity.grid(row=0,column=2)
    cart_label_frame.grid(row=8, column=2)
    shoppingcart_checkout_total.config(text=str(current_user.total))
    cart_button_frame.grid(row=10,column=2)
    signin_back_button.grid(row=10, column=0)
    cart_next.grid(row=9, column=2)
    cart_previous.grid(row=9, column=0)
    item_name_frame1.grid(row=2,column=0)
    item_name_frame2.grid(row=3,column=0)
    item_name_frame3.grid(row=4,column=0)
    item_name_frame4.grid(row=5,column=0)
    item_name_frame5.grid(row=6,column=0)
    item_name_frame6.grid(row=7,column=0)
    cart_item_price1.grid(row=2,column=1)
    cart_item_price2.grid(row=3,column=1)
    cart_item_price3.grid(row=4,column=1)
    cart_item_price4.grid(row=5,column=1)
    cart_item_price5.grid(row=6,column=1)
    cart_item_price6.grid(row=7,column=1)
    cart_item1_entry.grid(row=2,column=2)
    cart_item2_entry.grid(row=3,column=2)
    cart_item3_entry.grid(row=4,column=2)
    cart_item4_entry.grid(row=5,column=2)
    cart_item5_entry.grid(row=6,column=2)
    cart_item6_entry.grid(row=7,column=2)
    update_cart()

def update_total():
    set_cart_data()
    total_price = 0
    for e,f in zip(current_parameter.shopping_quantity_list, current_parameter.shopping_price_list):
        total_price += int(e)*int(f)
    current_user.total = total_price

def update_cart():
    update_quantity = [cart_item1_entry.get(), cart_item2_entry.get(), cart_item3_entry.get(), cart_item4_entry.get(), cart_item5_entry.get(), cart_item6_entry.get()]
    if current_parameter.current_cart_page != current_parameter.max_cart_page:
        for e in update_quantity:
            if not shop.check_quantity(e):
                return
        current_parameter.shopping_quantity_list[(current_parameter.current_cart_page-1)*6:(current_parameter.current_cart_page-1)*6+6] = update_quantity
    else:
        if cart_item6_entry["state"] == DISABLED:
            del update_quantity[5]
        if cart_item5_entry["state"] == DISABLED:
            del update_quantity[4]
        if cart_item4_entry["state"] == DISABLED:
            del update_quantity[3]
        if cart_item3_entry["state"] == DISABLED:
            del update_quantity[2]
        if cart_item2_entry["state"] == DISABLED:
            del update_quantity[1]
        if cart_item1_entry["state"] == DISABLED:
            del update_quantity[0]
        for e in update_quantity:
            if not shop.check_quantity(e):
                return
        current_parameter.shopping_quantity_list[(current_parameter.current_cart_page-1)*6:] = update_quantity
    current_user.shopping_cart = []
    for e,f in zip(current_parameter.shopping_quantity_list, current_parameter.shopping_did_list):
        for i in range(int(e)):
            current_user.shopping_cart.append(f)
    total_price = 0
    for e,f in zip(current_parameter.shopping_quantity_list, current_parameter.shopping_price_list):
        total_price += int(e)*int(f)
    current_user.total = total_price
    shop.write_cart(current_user.uid, current_user.shopping_cart)
    set_cart_data()
    cart_page_change()
    display_cart()
    shoppingcart_checkout_total.config(text=str(current_user.total))

def add_cart_button_action(i):
    reset_gui()
    shopping_image = dish_image_list[i]
    shopping_image.grid(row=0,column=0)
    shopping_name= dish_name_list[i]
    shopping_name.grid(row=1,column=0)
    shopping_price.append(current_parameter.price_list[i])
    dish_price_list[i].grid(row=2,column=0)
    shopping_did.append(dish_did_list[i])
    label_quantity_entry.grid(row=4,column=0)
    label_quantity.grid(row=3, column=0)
    signin_back_button.grid(row=6, column=0)
    shopping_enter_button.grid(row=5,column=0)

def shopping_enter_button_action():
    if current_user.uid != -1:
        if shop.check_quantity(label_quantity_entry.get()):
            for i in range(int(label_quantity_entry.get())):
                current_user.shopping_cart.append(shopping_did[-1])
                current_user.total += int(shopping_price[-1])
            messagebox.showinfo("", "Added to cart")
        label_quantity_entry.delete(0,END)
        shop.write_cart(current_user.uid, current_user.shopping_cart)
    else:
        messagebox.showwarning("", "Please log in first")

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
    for e in dish_comment_list:
        e.config(state=NORMAL)
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
    i=0
    for e in dish_did_list:
        if e == -1:
            dish_comment_list[i].config(state=DISABLED)
        i+=1

def cart_next_page():
    current_parameter.current_cart_page += 1
    cart_page_change()
    display_cart()

def cart_previous_page():
    current_parameter.current_cart_page -= 1
    cart_page_change()
    display_cart()

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
    signout_button.grid(row=0, column=0)
    delivery_order_listName.grid(row=1, column=0)
    delivery_order_list.grid(row=2, column=0)
    order_track_button.grid(row=3, column=0)
    order_list = element.get_order_list()
    delivery_order_list.delete(0,END)
    for item in order_list:
        delivery_order_list.insert(END, item)

def delivery_track_interface():
    reset_gui()
    node0.grid(row=0, column=0)
    node1.grid(row=0, column=2)
    node2.grid(row=0, column=4)
    node3.grid(row=0, column=6)
    node4.grid(row=0, column=8)
    node5.grid(row=2, column=0)    
    node6.grid(row=2, column=2)
    node7.grid(row=2, column=4)
    node8.grid(row=2, column=6)
    node9.grid(row=2, column=8)
    node10.grid(row=4, column=0)
    node11.grid(row=4, column=2)
    node12.grid(row=4, column=4)
    node13.grid(row=4, column=6)
    node14.grid(row=4, column=8)
    node15.grid(row=6, column=0)
    node16.grid(row=6, column=2)
    node17.grid(row=6, column=4)
    node18.grid(row=6, column=6)
    node19.grid(row=6, column=8)
    node20.grid(row=8, column=0)
    node21.grid(row=8, column=2)
    node22.grid(row=8, column=4)
    node23.grid(row=8, column=6)
    node24.grid(row=8, column=8)
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
    back_frame.grid(row=9, column=0, columnspan=10)

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
    i=0
    for e in dish_did_list:
        if e == -1:
            dish_comment_list[i].config(state=DISABLED)
        i+=1
    current_parameter.alldish = element.get_all_dish()
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
        info_button.grid(row=1, column=2)
        comment_button.grid(row=1, column=0)
        signout_button.grid(row=0, column=2)
    shopping_cart_items.grid(row=0, column=1)
    search_frame.grid(row=2, column=0, columnspan=3)
    dish_image1.grid(row=3, column=0)
    dish_name1.grid(row=4, column=0)
    dish_price1.grid(row=5, column=0)
    dish_buy1.grid(row=6, column=0)
    dish_comment1.grid(row=7, column=0)
    dish_image2.grid(row=3, column=1)
    dish_name2.grid(row=4, column=1)
    dish_price2.grid(row=5, column=1)
    dish_buy2.grid(row=6, column=1)
    dish_comment2.grid(row=7, column=1)
    dish_image3.grid(row=3, column=2)
    dish_name3.grid(row=4, column=2)
    dish_price3.grid(row=5, column=2)
    dish_buy3.grid(row=6, column=2)
    dish_comment3.grid(row=7, column=2)
    dish_image4.grid(row=8, column=0)
    dish_name4.grid(row=9, column=0)
    dish_price4.grid(row=10, column=0)
    dish_buy4.grid(row=11, column=0)
    dish_comment4.grid(row=12, column=0)
    dish_image5.grid(row=8, column=1)
    dish_name5.grid(row=9, column=1)
    dish_price5.grid(row=10, column=1)
    dish_buy5.grid(row=11, column=1)
    dish_comment5.grid(row=12, column=1)
    dish_image6.grid(row=8, column=2)
    dish_name6.grid(row=9, column=2)
    dish_price6.grid(row=10, column=2)
    dish_buy6.grid(row=11, column=2)
    dish_comment6.grid(row=12, column=2)
    next_page_button.grid(row=13, column=2)
    previous_page_button.grid(row=13, column=0)

def new_employee():
    reset_gui()
    employee_chef.config(state=NORMAL)
    employee_deliver.config(state=NORMAL)
    employee_back.grid(row=5, column=0)
    employee_type.grid(row=0, column=0)
    employee_type_frame.grid(row=0, column=1)
    employee_username.grid(row=2, column=1)
    employee_password.grid(row=3, column=1)
    employee_email.grid(row=4, column=1)
    employee_add.grid(row=5, column=1)
    employee_username_label.grid(row=2, column=0)
    employee_password_label.grid(row=3, column=0)
    employee_email_label.grid(row=4, column=0)
    employee_name_label.grid(row=1, column=0)
    employee_name.grid(row=1, column=1)

def select_type(t):
    if t == "c":
        current_parameter.employee_type = 1
        employee_chef.config(state=DISABLED)
        employee_deliver.config(state=NORMAL)
    else:
        current_parameter.employee_type = 2
        employee_chef.config(state=NORMAL)
        employee_deliver.config(state=DISABLED)

def register_new_employee():
    if employee_chef["state"] == "normal" and employee_deliver["state"] == "normal":
        messagebox.showwarning("", "Please select an employee type")
    else:
        signin.register_employee(current_parameter.employee_type, employee_name.get(), employee_username.get(), 
                            employee_password.get(), employee_email.get())
        employee_chef["state"] = "normal"
        employee_deliver["state"] = "normal"
        employee_email.delete(0,END)
        employee_name.delete(0,END)
        employee_password.delete(0,END)
        employee_username.delete(0,END)

def manager_interface():
    reset_gui()
    manage_employee.grid(row=0, column=1, columnspan=2)
    signout_button.grid(row=0, column=3)
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
    manager_approve_button.grid(row=9, column=3)
    manager_decline_button.grid(row=9, column=0)
    user_quit_label.grid(row=1, column=3)
    user_quit_list.grid(row=2, column=3)
    manager_update_all_action()

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
    user_quit_list.delete(0,END)
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
    quit_list = element.get_quit_list()
    for e in quit_list:
        user_quit_list.insert(END, e)
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
    except TclError:
        try:
            manage.approve_compliments(dish_compliments_list.get(dish_compliments_list.curselection()), input)
        except TclError:
            try:
                manage.approve_complaints(dish_complaints_list.get(dish_complaints_list.curselection()), input)
            except TclError:
                try:
                    manage.approve_pending_registrations(user_approved_list.get(user_approved_list.curselection()), input) 
                except TclError:
                    try:
                        manage.approve_pending_registrations(user_declined_list.get(user_declined_list.curselection()), input)        
                    except TclError:
                        try:
                            manage.approve_compliments(dish_approved_compliements_list.get(dish_approved_compliements_list.curselection()), input)            
                        except TclError:
                            try:
                                manage.approve_compliments(dish_declined_compliments_list.get(dish_declined_compliments_list.curselection()), input)                 
                            except TclError:
                                try:
                                    manage.approve_complaints(dish_approved_compliants_list.get(dish_approved_compliants_list.curselection()), input)                   
                                except TclError:
                                    try:
                                        manage.approve_complaints(dish_declined_compliants_list.get(dish_declined_compliants_list.curselection()), input)                       
                                    except TclError:
                                        try:
                                            if input == 1:
                                                manage.approve_pending_registrations(user_quit_list.get(user_quit_list.curselection()), 2)
                                            else:
                                                manage.approve_pending_registrations(user_quit_list.get(user_quit_list.curselection()), -2)                             
                                        except TclError:
                                            messagebox.showwarning("","Please select an item to process")
    manager_update_all_action()
    manage.auto_demote_promote_employee()
    manage.auto_vip_block()

def employee_management():
    reset_gui()
    employee_chef["state"] = "normal"
    employee_deliver["state"] = "normal"
    employee_email.delete(0,END)
    employee_name.delete(0,END)
    employee_password.delete(0,END)
    employee_username.delete(0,END)
    chef_employee_list.delete(0,END)
    dish_complaints_list.delete(0,END)
    deliver_employee_list.delete(0,END)
    add_employee.grid(row=0, column=0)
    chef_employee_list_label.grid(row=1, column=0)
    deliver_employee_list_label.grid(row=1, column=1)
    chef_employee_list.grid(row=2, column=0)
    deliver_employee_list.grid(row=2, column=1)
    management_back.grid(row=0, column=1)
    employee_promote.grid(row=3, column=1)
    employee_demote.grid(row=3, column=0)
    for item in element.get_chef_employee():
        chef_employee_list.insert(END, item)
    for item in element.get_deliver_employee():
        deliver_employee_list.insert(END, item)

def employee_salary_adjust(i):
    try:
        manage.demote_promote_employee(chef_employee_list.get(chef_employee_list.curselection()), i)
    except TclError:
        try:
            manage.demote_promote_employee(deliver_employee_list.get(deliver_employee_list.curselection()), i)
        except TclError:
            messagebox.showwarning("","Please select an item to process")
    chef_employee_list.selection_clear(0, END)
    deliver_employee_list.selection_clear(0, END)

def profile_button_action():
    reset_gui()
    profile_username_label.grid(row=0, column=0)
    profile_username.grid(row=0, column=1)
    profile_uid_label.grid(row=0, column=2)
    profile_uid.grid(row=0, column=3)
    profile_balance_label.grid(row=0, column=4)
    profile_balance.grid(row=0, column=5)
    profile_email_label.grid(row=0, column=6)
    profile_email.grid(row=0, column=7)
    profile_back_button.grid(row=1, column=9)
    profile_warning_label.grid(row=0, column=8)
    profile_warning.grid(row=0, column=9)
    profile_deposit_frame.grid(row=1,column=0, columnspan=9)
    profile = element.profile(current_user.uid)
    profile_username.config(text=profile[0])
    profile_uid.config(text=current_user.uid)
    profile_balance.config(text=profile[1])
    profile_email.config(text=profile[2])
    profile_warning.config(text=profile[3])

def make_deposit():
    element.deposit_money(profile_deposit.get(),current_user.uid)
    profile_deposit.delete(0,END)
    profile_button_action()

def view_comment(did):
    reset_gui()
    description_view.grid(row=3, column=0)
    description_view.config(text=element.get_description(did), wraplength=185, justify=LEFT)
    view_user_comment.grid(row=0, column=0, rowspan=2)
    view_star.grid(row=0, column=1)
    view_delivery.grid(row=1, column=1)
    profile_back_button.grid(row=3, column=1)
    data = element.comment_op(did)
    view_user_comment.delete(0,END)
    for e in data[0]:
        view_user_comment.insert(END, e)
    for e,f in zip(view_star_list, view_delivery_list):
        e.config(image=star_b)
        f.config(image=star_b)
    i=0
    for e in view_star_list:
        if i<data[1]:
            e.config(image=star_c)
        i+=1
    i=0
    for e in view_delivery_list:
        if i<data[2]:
            e.config(image=star_c)
        i+=1

def user_quit_action():
    if element.user_quit(current_user.uid):
        signout_button_action()

def search_button_action(text):
    found = False
    for e, did in current_parameter.alldish.items():
        if e == text:
            found = True
            temp = element.get_all(did)
    if not found:
        messagebox.showwarning("", "No dish named "+str(text))
    else:
        reset_gui()
        search_component[0] = PhotoImage(file=temp[2])
        shopping_image.config(image=search_component[0])
        shopping_image.grid(row=0,column=0)
        shopping_name.config(text=temp[0])
        shopping_name.grid(row=1,column=0)
        shopping_price.append(temp[1])
        dish_price.config(text=temp[1])
        dish_price.grid(row=2,column=0)
        shopping_did.append(did)
        label_quantity_entry.grid(row=4,column=0)
        label_quantity.grid(row=3, column=0)
        signin_back_button.grid(row=6, column=0)
        shopping_enter_button.grid(row=5,column=0)

def save_new_dish_action():
    element.save_new_dish(dish_name_entry.get(), price_entry.get(), description_entry.get(), image_entry.get())
    dish_name_entry.delete(0,END)
    price_entry.delete(0,END)
    description_entry.delete(0,END)
    image_entry.delete(0,END)

#view comment interface
star_c = PhotoImage(file="images/star_c.gif").subsample(5,5)
star_b = PhotoImage(file="images/star_b.gif").subsample(5,5)
view_user_comment = Listbox(program)
view_star = Frame(program)
view_delivery = Frame(program)
view_food_label = Label(view_star, text="Food")
view_delivery_label = Label(view_delivery, text="Delivery")
view_star1 = Label(view_star, image=star_b)
view_star2 = Label(view_star, image=star_b)
view_star3 = Label(view_star, image=star_b)
view_star4 = Label(view_star, image=star_b)
view_star5 = Label(view_star, image=star_b)
view_star_list = [view_star1, view_star2, view_star3, view_star4, view_star5]
view_delivery1 = Label(view_delivery, image=star_b)
view_delivery2 = Label(view_delivery, image=star_b)
view_delivery3 = Label(view_delivery, image=star_b)
view_delivery4 = Label(view_delivery, image=star_b)
view_delivery5 = Label(view_delivery, image=star_b)
view_delivery_list = [view_delivery1, view_delivery2, view_delivery3, view_delivery4, view_delivery5]
view_food_label.pack(side="left")
view_star1.pack(side="left")
view_star2.pack(side="left")
view_star3.pack(side="left")
view_star4.pack(side="left")
view_star5.pack(side="left")
view_delivery_label.pack(side="left")
view_delivery1.pack(side="left")
view_delivery2.pack(side="left")
view_delivery3.pack(side="left")
view_delivery4.pack(side="left")
view_delivery5.pack(side="left")
description_view = Label(program)

#comment interface
combined_rate_frame = Frame(program)
star_food_frame = Frame(combined_rate_frame)
star_delivery_frame = Frame(combined_rate_frame)
rate_button_frame = Frame(combined_rate_frame)
rate_food_back = Button(rate_button_frame, text="Back", command=start_interface)
rate_food = Button(rate_button_frame, text="Submit", command=submit_rating)
rate_food_back.pack(side="left")
rate_food.pack(side="left")
rate_comment_frame = Frame(combined_rate_frame)
rate_comment_label = Label(rate_comment_frame, text="Comment")
rate_comment = Entry(rate_comment_frame)
rate_comment_label.pack(side="left")
rate_comment.pack(side="left")
star_food_frame.pack(side="top")
star_delivery_frame.pack(side="top")
rate_comment_frame.pack(side="top")
rate_button_frame.pack(side="top")
rate_food.pack(side="top")
star_food_label = Label(star_food_frame, text="Food")
star1_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(1))
star2_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(2))
star3_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(3))
star4_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(4))
star5_food = Button(star_food_frame, image=star_b, command=lambda: star_food_change(5))
star_food_list = [star1_food, star2_food, star3_food, star4_food, star5_food]
star_food_label.pack(side="left")
star1_food.pack(side="left")
star2_food.pack(side="left")
star3_food.pack(side="left")
star4_food.pack(side="left")
star5_food.pack(side="left")
star_delivery_label = Label(star_delivery_frame, text="Delivery")
star1_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(1))
star2_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(2))
star3_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(3))
star4_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(4))
star5_delivery = Button(star_delivery_frame, image=star_b, command=lambda: star_delivery_change(5))
star_delivery_list = [star1_delivery, star2_delivery, star3_delivery, star4_delivery, star5_delivery]
star_delivery_label.pack(side="left")
star1_delivery.pack(side="left")
star2_delivery.pack(side="left")
star3_delivery.pack(side="left")
star4_delivery.pack(side="left")
star5_delivery.pack(side="left")
order_history_label = Label(program, text="Unrated order")
rate_order_list = Listbox(program)

#user profile
profile_username_label = Label(program, text="Username")
profile_username = Button(text="", command=None)
profile_uid_label = Label(program, text="ID")
profile_uid = Button(text="", command=None)
profile_balance_label = Label(program, text="Balance")
profile_balance = Button(text="", command=None)
profile_email_label = Label(program, text="Email")
profile_email = Button(text="", command=None)
profile_back_button = Button(text="Back", command = start_interface)
profile_deposit_frame = Frame(program)
profile_deposit = Entry(profile_deposit_frame)
profile_deposit_button = Button(profile_deposit_frame, text="Deposit", command=make_deposit)
profile_warning_label = Label(program, text="Warning")
profile_warning = Button(text="", command=None)
profile_deposit.pack(side="left")
profile_deposit_button.pack(side="left")
profile_user_quit = Button(profile_deposit_frame, text="Close account", command= user_quit_action)
profile_user_quit.pack(side="left")

#chef interface
available_dish_list = Listbox(program)
current_dish_list = Listbox(program)
available_dish_label = Label(program, text="Available dish")
current_dish_label = Label(program, text="Current dish")
add_new_dish_button_label = Label(program, text="Add new dish")
add_new_dish_button = Button(text="Add new dish", command=add_new_dish_interface)
chef_frame = Frame(program)
save_menu_button = Button(text="Save", command=save_menu_action)
dish_add = Button(chef_frame, text="Add ->", command=add_dish)
dish_remove = Button(chef_frame, text="<- Remove", command=remove_dish)
dish_add.pack(side="top")
dish_remove.pack(side="top")

#add new dish interface
add_back_button = Button(text="Back", command=chef_interface)
dish_name_label = Label(program, text="Name")
price_label = Label(program, text="Price $")
description_label = Label(program, text="Description")
image_label = Label(program, text="Image")
dish_name_entry = Entry(program)
price_entry = Entry(program)
description_entry = Entry(program)
image_entry = Entry(program)
save_button = Button(text="Save", command= save_new_dish_action)

#manager interface
management_back = Button(text="Back", command=manager_interface)
deliver_employee_list_label = Label(program, text="Deliver")
chef_employee_list_label = Label(program, text="Chef")
chef_employee_list = Listbox(program)
deliver_employee_list = Listbox(program)
employee_promote = Button(text="Promote", command=lambda: employee_salary_adjust(1))
employee_demote = Button(text="Demote", command=lambda: employee_salary_adjust(-1))
manage_employee = Button(text="Manage employees", command=employee_management)
employee_type_frame = Frame(program)
employee_chef = Button(employee_type_frame, text="Chef", command=lambda: select_type("c"))
employee_back = Button(text="Back", command=employee_management)
employee_deliver = Button(employee_type_frame, text="Deliver", command=lambda: select_type("d"))
employee_chef.pack(side="left")
employee_deliver.pack(side="left")
employee_username = Entry(program)
employee_password = Entry(program)
employee_email = Entry(program)
employee_add = Button(text="Add", command=register_new_employee)
employee_username_label = Label(program, text="Username")
employee_password_label = Label(program, text="Password")
employee_email_label = Label(program, text="Email")
employee_name_label = Label(program, text="Name")
employee_name = Entry(program)
employee_type = Label(program, text="Type")
add_employee = Button(text="Add employee", command=new_employee)
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
user_quit_label = Label(program, text="Closing accountss")
user_quit_list = Listbox(program)

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

#shopping cart interface
photo=""
search_component = [photo]
dish_price = Label(program, text="")
cart_next = Button(program, text="Next", command=cart_next_page)
cart_previous = Button(program, text="Previous", command=cart_previous_page)
label_quantity_entry = Entry(program)
label_quantity = Label(program, text="Quantity")
shopping_enter_button = Button(text="Enter", command=shopping_enter_button_action)
shopping_image = Label(image=None)
shopping_did = []
shopping_name = Label(program, text="")
shopping_price=[]
shopping_quantity=[]
cart_button_frame = Frame(program)
shoppingcart_checkout_button=Button(cart_button_frame, text="Check out",command=shoppingcart_checkout_button_action)
cart_update = Button(cart_button_frame, text="Update", command=update_cart)
cart_update.pack(side="left")
shoppingcart_checkout_button.pack(side="left")
cart_label_frame = Frame(program)
shoppingcart_checkout_total= Label(cart_label_frame,text=0)
shoppingcart_checkout_total_label = Label(cart_label_frame, text="Total:")
shoppingcart_checkout_total_label.pack(side="left")
shoppingcart_checkout_total.pack(side="left")
label_shoppingcart_item =Label(program,text="Item")
label_shoppingcart_price =Label(program,text="Unit Price")
label_shoppingcart_quantity =Label(program,text="Quantity")
label_shoppingcart_sumnarry =Label(program,text="Your order summury:")
item_name_frame1 = Frame(program)
item_name_frame2 = Frame(program)
item_name_frame3 = Frame(program)
item_name_frame4 = Frame(program)
item_name_frame5 = Frame(program)
item_name_frame6 = Frame(program)
cart_item1_image = Label(item_name_frame1, image=None)
cart_item2_image = Label(item_name_frame2, image=None)
cart_item3_image = Label(item_name_frame3, image=None)
cart_item4_image = Label(item_name_frame4, image=None)
cart_item5_image = Label(item_name_frame5, image=None)
cart_item6_image = Label(item_name_frame6, image=None)
shopping_name_label1 = Label(item_name_frame1, text="Name")
shopping_name_label2 = Label(item_name_frame2, text="Name")
shopping_name_label3 = Label(item_name_frame3, text="Name")
shopping_name_label4 = Label(item_name_frame4, text="Name")
shopping_name_label5 = Label(item_name_frame5, text="Name")
shopping_name_label6 = Label(item_name_frame6, text="Name")
cart_item1_image.pack(side="left")
cart_item2_image.pack(side="left")
cart_item3_image.pack(side="left")
cart_item4_image.pack(side="left")
cart_item5_image.pack(side="left")
cart_item6_image.pack(side="left")
shopping_name_label1.pack(side="left")
shopping_name_label2.pack(side="left")
shopping_name_label3.pack(side="left")
shopping_name_label4.pack(side="left")
shopping_name_label5.pack(side="left")
shopping_name_label6.pack(side="left")
cart_item_price1 = Label(program, text="Price")
cart_item_price2 = Label(program, text="Price")
cart_item_price3 = Label(program, text="Price")
cart_item_price4 = Label(program, text="Price")
cart_item_price5 = Label(program, text="Price")
cart_item_price6 = Label(program, text="Price")
cart_item1_entry = Entry(program)
cart_item2_entry = Entry(program)
cart_item3_entry = Entry(program)
cart_item4_entry = Entry(program)
cart_item5_entry = Entry(program)
cart_item6_entry = Entry(program)
cart_item_price_list = [cart_item_price1, cart_item_price2, cart_item_price3, cart_item_price4, cart_item_price5, cart_item_price6]
cart_item_image_list = [cart_item1_image, cart_item2_image, cart_item3_image, cart_item4_image, cart_item5_image, cart_item6_image]
shopping_name_label_list = [shopping_name_label1, shopping_name_label2, shopping_name_label3, shopping_name_label4, shopping_name_label5, shopping_name_label6]
cart_item_entry_list = [cart_item1_entry, cart_item2_entry, cart_item3_entry, cart_item4_entry, cart_item5_entry, cart_item6_entry]
cart_did_list1 = ""
cart_did_list2 = ""
cart_did_list3 = ""
cart_did_list4 = ""
cart_did_list5 = ""
cart_did_list6 = ""
cart_image1 = Label(image=None)
cart_image2 = Label(image=None)
cart_image3 = Label(image=None)
cart_image4 = Label(image=None)
cart_image5 = Label(image=None)
cart_image6 = Label(image=None)
cart_image_list = [cart_image1, cart_image2, cart_image3, cart_image4, cart_image5, cart_image6]
cart_did_list = [cart_did_list1, cart_did_list2, cart_did_list3, cart_did_list4, cart_did_list5, cart_did_list6]

#delivery interface
delivery_order_list = Listbox(program)
delivery_order_listName = Label(program, text="Order list")
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
edge_matrix[0][1] = edge1
edge_matrix[1][2] = edge2
edge_matrix[2][3] = edge3
edge_matrix[3][4] = edge4
edge_matrix[0][5] = edge5
edge_matrix[1][6] = edge6
edge_matrix[2][7] = edge7
edge_matrix[3][8] = edge8
edge_matrix[4][9] = edge9
edge_matrix[5][6] = edge10
edge_matrix[6][7] = edge11
edge_matrix[7][8] = edge12
edge_matrix[8][9] = edge13
edge_matrix[5][10] = edge14
edge_matrix[6][11] = edge15
edge_matrix[7][12] = edge16
edge_matrix[8][13] = edge17
edge_matrix[9][14] = edge18
edge_matrix[10][11] = edge19
edge_matrix[11][12] = edge20
edge_matrix[12][13] = edge21
edge_matrix[13][14] = edge22
edge_matrix[10][15] = edge23
edge_matrix[11][16] = edge24
edge_matrix[12][17] = edge25
edge_matrix[13][18] = edge26
edge_matrix[14][19] = edge27
edge_matrix[15][16] = edge28
edge_matrix[16][17] = edge29
edge_matrix[17][18] = edge30
edge_matrix[18][19] = edge31
edge_matrix[15][20] = edge32
edge_matrix[16][21] = edge33
edge_matrix[17][22] = edge34
edge_matrix[18][23] = edge35
edge_matrix[19][24] = edge36
edge_matrix[20][21] = edge37
edge_matrix[21][22] = edge38
edge_matrix[22][23] = edge39
edge_matrix[23][24] = edge40
delivery_order_listName = Label(program, text="Order list")
signout_button = Button(text="Sign Out", command=signout_button_action)
order_track_button = Button(text="Track", command=delivery_track_interface)

#start interface
search_frame = Frame(program)
search_entry = Entry(search_frame)
search_button = Button(search_frame, text="Search", command = lambda: search_button_action(search_entry.get()))
search_entry.pack(side="left")
search_button.pack(side="left")
chef_name = Label(program, text="All")
info_button = Button(text="Profile", command=profile_button_action)
comment_button = Button(text="Comment", command=comment_interface)
refresh_button = Button(text="Refresh", command=refresh_menu)
shopping_cart_items = Button(text="Your Shopping Cart", command=shopping_cart_button_action)
signout_button = Button(text="Sign Out", command=signout_button_action)
signin_button = Button(text="Sign In", command=signin_interface)
next_page_button = Button(text="Next", command=menu_next_page)
previous_page_button = Button(text="Previous", command=menu_previous_page)
etc_photo = PhotoImage(file="images/etc.gif")
etc_photo_small = PhotoImage(file="images/etc.gif").subsample(2,2)
dish_image1 = Label(image=None)
dish_name1 = Label(program, text="Name")
dish_price1 = Label(program, text="Price")
dish_buy1 = Button(text="Add to cart", command=lambda: add_cart_button_action(0))
dish_did1=""
dish_comment1 = Button(text="View", command=lambda: view_comment(dish_did_list[0]))
dish_image2 = Label(image=None)
dish_name2 = Label(program, text="Name")
dish_price2 = Label(program, text="Price")
dish_buy2 = Button(text="Add to cart", command=lambda: add_cart_button_action(1))
dish_did2=""
dish_comment2 = Button(text="View", command=lambda: view_comment(dish_did_list[1]))
dish_image3 = Label(image=None)
dish_name3 = Label(program, text="Name")
dish_price3 = Label(program, text="Price")
dish_buy3 = Button(text="Add to cart", command=lambda: add_cart_button_action(2))
dish_did3=""
dish_comment3 = Button(text="View", command=lambda: view_comment(dish_did_list[2]))
dish_image4 = Label(image=None)
dish_name4 = Label(program, text="Name")
dish_price4 = Label(program, text="Price")
dish_buy4 = Button(text="Add to cart", command=lambda: add_cart_button_action(3))
dish_did4=""
dish_comment4 = Button(text="View", command=lambda: view_comment(dish_did_list[3]))
dish_image5 = Label(image=None)
dish_name5 = Label(program, text="Name")
dish_price5 = Label(program, text="Price")
dish_buy5 = Button(text="Add to cart", command=lambda: add_cart_button_action(4))
dish_did5=""
dish_comment5 = Button(text="View", command=lambda: view_comment(dish_did_list[4]))
dish_image6 = Label(image=None)
dish_name6 = Label(program, text="Name")
dish_price6 = Label(program, text="Price")
dish_buy6 = Button(text="Add to cart", command=lambda: add_cart_button_action(5))
dish_did6=""
dish_comment6 = Button(text="View", command=lambda: view_comment(dish_did_list[5]))
img1=""
img2=""
img3=""
img4=""
img5=""
img6=""
dish_comment_list = [dish_comment1, dish_comment2, dish_comment3, dish_comment4, dish_comment5, dish_comment6]
dish_image_list = [dish_image1, dish_image2, dish_image3, dish_image4, dish_image5, dish_image6]
dish_buy_list = [dish_buy1, dish_buy2, dish_buy3, dish_buy4, dish_buy5, dish_buy6]
dish_did_list = [dish_did1, dish_did2, dish_did3, dish_did4, dish_did5, dish_did6]
dish_name_list = [dish_name1, dish_name2, dish_name3, dish_name4, dish_name5, dish_name6]
dish_price_list = [dish_price1, dish_price2, dish_price3, dish_price4, dish_price5, dish_price6]
dish_img_list = [img1, img2, img3, img4, img5, img6]

start_interface()
manage.auto_demote_promote_employee()
manage.auto_vip_block()
program.mainloop()