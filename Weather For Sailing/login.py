from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import Image, ImageTk
import os
import subprocess


def validate_login(username, password):
    # Check if the username and password are valid
    with open('db/users.txt', 'r') as file:
        for line in file:
            user_data = line.strip().split(',')
            if len(user_data) == 3:
                saved_username, saved_password, user_id = user_data
                if username == saved_username and password == saved_password:
                    print("Login successful!")
                    user_file = open("last_user.txt", "r+")
                    user_file.write(saved_username.strip())
                    user_file.close()
                    return
        print("Invalid username or password")

def sign_up():
    # Close the current program
    tkWindow.destroy()  

    # Run signup.py
    subprocess.Popen(["python", "signup.py"])

# Window
tkWindow = Tk()
tkWindow.title('Weather For Sailors')
tkWindow.geometry("700x700")
tkWindow.resizable(width=False, height=False)

# Background Image
ocean_image = PhotoImage(file="/Users/logan/Documents/Weather For Sailing/assets/photoImageLogInPage.png")
ocean_image_label = Label(tkWindow, image=ocean_image)
ocean_image_label.place(x=0, y=0)

# Logo Image
boat_logo = Image.open("/Users/logan/Documents/Weather For Sailing/assets/Sailing App logo.png")
boat_logo = boat_logo.resize((200, 200)) 
boat_logo = ImageTk.PhotoImage(boat_logo)
boat_logo_label = Label(tkWindow, image=boat_logo)
boat_logo_label.place(relx=0.5, rely=0.3, anchor=CENTER)

# Username Label and Text Entry Box
username_label = Label(tkWindow, text="Username:")
username_label.place(relx=0.5, rely=0.48, anchor=CENTER)
username = StringVar()
username_entry = Entry(tkWindow, textvariable=username)
username_entry.place(relx=0.5, rely=0.52, anchor=CENTER)

# Password Label and Text Entry Box
password_label = Label(tkWindow, text="Password:")
password_label.place(relx=0.5, rely=0.57, anchor=CENTER)
password = StringVar()
password_entry = Entry(tkWindow, textvariable=password, show="*")
password_entry.place(relx=0.5, rely=0.61, anchor=CENTER)

# Login Button
validate_login = partial(validate_login, username, password)
login_button = Button(tkWindow, text="Log in", command=validate_login)
login_button.place(relx=0.5, rely=0.65, anchor=CENTER)

# Sign Up Button
sign_up_button = Button(tkWindow, text="Sign Up", command=sign_up)
sign_up_button.place(relx=0.5, rely=0.69, anchor=CENTER)

tkWindow.mainloop()
