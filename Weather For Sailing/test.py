from tkinter import *
import tkinter.font as font
import threading
import time
import requests
import tk 
import tkinter as tk
from datetime import datetime

user_file = open("last_user.txt", "r+")
lines = user_file.readlines()

for username in lines:
    if username.strip():
        logged_in_username = username.strip()
        break

user_file.close()

if not (logged_in_username == ""):
    choices_file = open("db/choices.txt", "r+")
    choices_lines = choices_file.readlines()

    for line in choices_lines:
        if (logged_in_username.strip() in line):
            user_choices_string = line.split("=")
            logged_in_user_choice1 = user_choices_string[1].strip()
            logged_in_user_choice2 = user_choices_string[2].strip()
            logged_in_user_choice3 = user_choices_string[3].strip()

            print(logged_in_user_choice1, logged_in_user_choice2, logged_in_user_choice3)
            break

    choices_file.close()

def get_wind_speed_category(speed):
    if speed < 5:
        return "light"
    elif 6 <= speed <= 14:
        return "normal"
    else:
        return "windy"

def get_tide_data():
    response = requests.get(tide_url)
    data = response.json()
    return data["values"]

def find_next_high_low_tides(tide_data):
    high_tides = []
    low_tides = []
    
    for entry in tide_data:
        if entry["value"] > 2.0:
            high_tides.append(entry)
        elif entry["value"] < 1.0:
            low_tides.append(entry)
    
    return high_tides, low_tides

def get_time_string(timestamp):
    time = datetime.fromisoformat(timestamp[:-1])
    return time.strftime("%H:%M")

def wind_info(response):
    wind_speed = response['wind']['speed']
    # Convert wind speed from m/s to knots
    wind_speed *= 1.944 
    #Remove excess decimal
    formated_wind_speed = f"{wind_speed:.3g}"
    sailing_variable1.config(text="Wind Speed: {} knots".format(formated_wind_speed))

def temp_info(temperature_variable):
    temp_value = response['main']['temp']
    temp_value -= 273.15
    formated_temp_value = f"{temp_value:.3g}"
    temperature_variable.config(text = "Current temperature:  " + str(formated_temp_value) + "°C")
    print(response)

def weather_info(temperature_variable):
    weather_value = response['main']['temp']
    temperature_variable.config(text = "Current temperature:  " + str(weather_value) + "°C")


def display_next_tides(tide_data):
    high_tides, low_tides = find_next_high_low_tides(tide_data)
    find_next_high_low_tides(tide_data)
    next_high_tide = high_tides[0] if high_tides else None
    next_low_tide = low_tides[0] if low_tides else None
    tide_label.config(text=f"Next High Tide: {get_time_string(next_high_tide['time'])}\nNext Low Tide: {get_time_string(next_low_tide['time'])}")

def tide_info(timestamp, tide_data, high_tides, low_tides):
    get_time_string(timestamp)
    display_next_tides(tide_data)
    next_high_tide = high_tides[0] if high_tides else None
    next_low_tide = low_tides[0] if low_tides else None
    tide_label.config(text=f"Next High Tide: {get_time_string(next_high_tide['time'])}\nNext Low Tide: {get_time_string(next_low_tide['time'])}")

    
def get_weather_and_tide_info(city, api_key, tide_url):
    base_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, api_key)
    response = requests.get(base_weather_url).json()

    wind_info(response)  # Update wind information first
    
    # Get tide data
    tide_data = get_tide_data()  # Call get_tide_data() without any arguments
    high_tides, low_tides = find_next_high_low_tides(tide_data)

    # Pass tide_data to display_next_tides function
    display_next_tides(tide_data)

    next_high_tide = high_tides[0] if high_tides else None
    next_low_tide = low_tides[0] if low_tides else None

    tide_label.config(text=f"Next High Tide: {get_time_string(next_high_tide['time'])}\nNext Low Tide: {get_time_string(next_low_tide['time'])}")
    
    
    gory = get_wind_speed_category(float(sailing_variable1["text"].split()[2]))
    condition_text.set("Sailing is " + wind_category + " today")

#below are functions used to place weather info into the frames (in the order which the user picked)
def choice_wind_speed():
    sailing_variable1 = Label(frame1, fg="white", bg="#0b419e", font=bold_font)
    sailing_variable1.place(x=10, y=10)

def choice_tide_time():
    tide_label = Label(tide_variable, text="", font=bold_font, bg= "#2473d4", fg="white")
    tide_label.pack()

def choice_temp():
    temperature_variable = Label(frame3, fg="white",bg="#40aadb" ,font=bold_font)
    temperature_variable.place(x=10, y=10)

# Define the api key and city
city = 'Auckland'
api_key = "9522fe2047582e922d19ac9849c35ee6"
tide_url = "https://api.niwa.co.nz/tides/data?lat=-36.8667&long=174.7667&apikey=AVSnwX4R53kB1Yh17vY2zs1qGibFGw0Y"

# Create the Tkinter window
tkWindow = Tk()
tkWindow.geometry("1400x800")
tkWindow.title('Weather For Sailors')

# Defining the fonts
normal_font = font.Font(family="Arial", size=20)


# Frame 1: Weather Module 1
frame1 = Frame(tkWindow, bg="#0b419e", width=450, height=660)
frame1.place(x=10, y=100)

# Frame 2: Weather Module 2
frame2 = Frame(tkWindow, bg="#2473d4", width=470, height=660)
frame2.place(x=470, y=100)

# Frame 3: Weather Module 3
frame3 = Frame(tkWindow, bg="#40aadb", width=440, height=660)
frame3.place(x=949, y=100)

bold_font = font.Font(family="Arial", size=24, weight="bold")

# Call weather info for first frame (based on user choice)
choice_wind_speed()

# Call weather info for second frame (based on user choice)
choice_tide_time()

# Call weather info for third frame (based on user choice)
choice_temp()

# Define UI elements
sailing_variable1 = Label(frame1, fg="white", bg="#0b419e", font=bold_font)  # Corrected placement
sailing_variable1.place(x=10, y=10)

tide_variable = Frame(frame2, bg="#2473d4")  # Create the tide_variable frame
tide_label = Label(tide_variable, text="", font=bold_font, bg="#2473d4", fg="white")
tide_label.pack()


condition_text = StringVar()
condition_text.set("")

# Call the master function to get all data and update the UI
get_weather_and_tide_info(city, api_key, tide_url)


# Define the api key
city = 'Auckland'
api_key = "9522fe2047582e922d19ac9849c35ee6"

# Define the base url for the point forecast api
base_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, api_key)
tide_url = "https://api.niwa.co.nz/tides/data?lat=-36.8667&long=174.7667&apikey=AVSnwX4R53kB1Yh17vY2zs1qGibFGw0Y"

# window
response = requests.get(base_weather_url).json()
wind_speed = response['wind']['speed']
wind_category = get_wind_speed_category(wind_speed)
condition_text.set("Sailing is " + wind_category + " today")

title_lable = Label(tkWindow, textvariable=condition_text, font=("Arial", 50))
title_lable.place(relx=0.5, y=45, anchor=tk.CENTER)

temp_info()

tkWindow.mainloop()