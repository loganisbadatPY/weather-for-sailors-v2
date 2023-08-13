from email import message
from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import os
import random
import string
import subprocess

# Function to handle sign-up button click
def sign_up():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        if not check_user_exists(username):
            # Generate user ID
            user_id = generate_user_id(username)
            
            # Password requirements check
            if (
                len(password) < 8
                or not any(char.isupper() for char in password)
                or not any(char.isdigit() for char in password)
            ):
                messagebox.showerror(
                    "Error",
                    "Password must have at least 8 characters, "
                    "including at least one capital letter and one number.",
                )
                return

            # Add username, password, and user ID to the database
            if re.match("^[a-zA-Z0-9_]+$", username):
                add_user_to_database(username, password, user_id)
 
                 # Show success message
                messagebox.showinfo("Success", "Sign up successful!")
                tkWindow.destroy() 
                subprocess.Popen(["python", "choice_selector.py"])

                user_file = open("last_user.txt", "r+")
                for line in user_file.readlines():
                    line = ""
                    break
                user_file.write(username.strip())
                user_file.close()

                #import choice_selector     
            else:
                messagebox.showerror("Error", "Username Contains Invalid Characters")
                return
        else:
            # Show error message if user already exists
            messagebox.showerror("Error", "Username already exists!")
            return
    else:
        # Show error message if username or password is empty
        messagebox.showerror("Error", "Please enter both username and password!")
        return

    if username and password:
        if not check_user_exists(username):
            # Generate user ID
            user_id = generate_user_id(username)
    
    if username and password:
        if not check_user_exists(username):
            # Generate user ID
            user_id = generate_user_id(username)
            
            # Add username, password, and user ID to the database
            if re.match("^[a-zA-Z0-9_]+$", username):
                add_user_to_database(username, password, user_id)

                user_file = open("last_user.txt", "r+")
                for line in user_file.readlines():
                    print(line)
                    break
                user_file.write(username.strip())
                user_file.close()

                 # Show success message
                messagebox.showinfo("Success", "Sign up successful!")
                tkWindow.destroy() 
                subprocess.callr(["python", "choice_selector.py"])

                

                #import choice_selector     
            else:
                messagebox.showerror("Error", "Username Contains Invalid Characters")
                return
           
        else:
            # Show error message if user already exists
            messagebox.showerror("Error", "Username already exists!")
            return
    else:
        # Show error message if username or password is empty
        messagebox.showerror("Error", "Please enter both username and password!")
        return

# Function to check if a username already exists in the database
def check_user_exists(username):
    with open("db/users.txt", "r") as file:
        for line in file:
            line_list = line.split(",")
            if username.strip() == line_list[0].strip():
                return True
    return False

# Function to generate a user ID
def generate_user_id(username):
    random_chars = random.choices(string.ascii_letters + string.digits, k=5)
    user_id = username + ''.join(random_chars)
    return user_id

# Function to add a user to the database
def add_user_to_database(username, password, user_id):
    with open("db/users.txt", "a") as file:
        file.write(f"{username},{password},{user_id}\n")

# Window
tkWindow = Tk()
tkWindow.title('Weather For Sailors')
tkWindow.geometry("700x700")
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth() 
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry("{}x{}+{}+{}".format(width,height,x,y))
    
center_window(tkWindow)
tkWindow.resizable(width=False, height=False)

# Background Image
ocean_image = PhotoImage(file="assets/photoImageLogInPage.png")
ocean_image_label = Label(tkWindow, image=ocean_image)
ocean_image_label.place(x=0, y=0)

# Logo Image
boat_logo = Image.open("assets/Sailing App logo.png")
boat_logo = boat_logo.resize((200, 200))
boat_logo = ImageTk.PhotoImage(boat_logo)
boat_logo_label = Label(tkWindow, image=boat_logo)
boat_logo_label.place(relx=0.5, rely=0.3, anchor=CENTER)

# Username Label and Entry
username_label = Label(tkWindow, text="Username:")
username_label.place(relx=0.5, rely=0.5, anchor=CENTER)
username_entry = Entry(tkWindow)
username_entry.place(relx=0.5, rely=0.55, anchor=CENTER)

# Password Label and Entry
password_label = Label(tkWindow, text="Password:")
password_label.place(relx=0.5, rely=0.6, anchor=CENTER)
password_entry = Entry(tkWindow, show="*")
password_entry.place(relx=0.5, rely=0.65, anchor=CENTER)

# Sign Up Button
sign_up_button = Button(tkWindow, text="Sign Up", command=sign_up)
sign_up_button.place(relx=0.5, rely=0.7, anchor=CENTER)

tkWindow.mainloop()