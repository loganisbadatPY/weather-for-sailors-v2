from logging import RootLogger
import tkinter as tk

from tkinter import *
from tkinter import messagebox

# Set the directory path
directory_path = "/Users/logan/Documents/Weather For Sailing"
logged_in_username = ""


# Function to save the selected choices
def save_choices():
    # Get the selected choices from the choice variables
    selected_choices = []
    for choice_var in choice_vars:
        if choice_var.get() != 0:
            selected_choices.append(choices[choice_vars.index(choice_var)])

    # Check if exactly three choices are selected
    if len(selected_choices) == 3:
        # Open the choices.txt file in write mode
        logged_in_username = ""

        user_file = open("last_user.txt", "r+")
        lines = user_file.readlines()

        for username in lines:
            if username.strip():
                logged_in_username = username.strip()
                break

        if logged_in_username == "":
            messagebox.showinfo("Error", "User log-in invalid.")
            return

        user_file.close()

        user_found = BooleanVar()
        user_found.set(False)

        user_data = open("db/choices.txt", "r+")
        lines = user_data.readlines()

        for index, line in enumerate(lines):
            if logged_in_username.upper().strip() in line:
                user_found.set(True)
                new_line = "{},{},{},{}\n".format(logged_in_username.strip(), selected_choices[0], selected_choices[1], selected_choices[2])

                lines[index] = new_line
                user_data.seek(0)

                user_data.writelines(lines)
                user_data.truncate()
                break

        if not user_found.get():
            user_data.write("{}={}={}={}\n".format(logged_in_username.strip(), selected_choices[0], selected_choices[1], selected_choices[2]))
            user_data.close()

        # Show a success message box
        messagebox.showinfo("Success", "Choices saved successfully!")

        # Close the tkinter window
        root.destroy()

        # Import the home module (assuming it exists)
        import home
    else:
        # Show a warning message box for invalid selection
        messagebox.showwarning("Invalid Selection", "Please select exactly three choices.")


# Create the root tkinter window
root = tk.Tk()
root.title("Choice Selection")
root.geometry("300x250")
root.resizable(width=False, height=False)

# Function to center the window on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))

# Call the center_window function to center the window
center_window(root)

# Available choices
choices = ["Windspeed", "Tide", "Windgusts", "Current", "Weather", "Temperature"]

# Create choice variables
choice_vars = []
for i, choice in enumerate(choices):
    choice_var = tk.IntVar(value=0)  # Initialize as 0 (off)
    choice_vars.append(choice_var)

    # Create a check button for each choice
    checkbox = tk.Checkbutton(root, text=choice, variable=choice_var)
    checkbox.pack(anchor=tk.W)

# Create a button to save the choices
save_button = tk.Button(root, text="Save", command=save_choices)
save_button.pack(pady=10)

# Start the tkinter event loop
root.mainloop()