from tkinter import *
import tkinter.font as font
import requests
from datetime import datetime

TIDE_API_URL = "https://api.niwa.co.nz/tides/data?lat=-36.8667&long=174.7667&apikey=AVSnwX4R53kB1Yh17vY2zs1qGibFGw0Y"
WEATHER_API_KEY = "9522fe2047582e922d19ac9849c35ee6"
CITY = "Auckland"

def get_weather_conditions():
    base_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}"
    response = requests.get(base_weather_url).json()
    wind_speed = response['wind']['speed']
    temperature = response['main']['temp']
    return wind_speed, temperature


def get_tide_data():
    response = requests.get(TIDE_API_URL)
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

def display_next_tides():
    tide_data = get_tide_data()
    high_tides, low_tides = find_next_high_low_tides(tide_data)
    
    next_high_tide = high_tides[0] if high_tides else None
    next_low_tide = low_tides[0] if low_tides else None
    
    high_tide_label.config(text=f"Next High Tide: {get_time_string(next_high_tide['time'])}" if next_high_tide else "No High Tide Today")
    low_tide_label.config(text=f"Next Low Tide: {get_time_string(next_low_tide['time'])}" if next_low_tide else "No Low Tide Today")

def choice_wind_speed(wind_speed):
    sailing_variable1 = Label(frame1, text=f"Wind Speed: {wind_speed} m/s", fg="white", bg="#0b419e", font=bold_font)
    sailing_variable1.place(x=10, y=10)

def choice_tide_time():
    tide_variable = Frame(frame2, bg="#2473d4", width=470, height=660)
    tide_variable.place(x=0, y=0)

    global high_tide_label, low_tide_label
    high_tide_label = Label(tide_variable, text="", font=bold_font, bg="#2473d4", fg="white")
    high_tide_label.place(x=10, y=10)
    
    low_tide_label = Label(tide_variable, text="", font=bold_font, bg="#2473d4", fg="white")
    low_tide_label.place(x=10, y=50)

    display_next_tides()

def choice_temperature(temperature):
    temperature_variable = Label(frame3, text=f"Temperature: {temperature} °C", fg="white", bg="#40aadb", font=bold_font)
    temperature_variable.place(x=10, y=10)

# Create the Tkinter window
tkWindow = Tk()
tkWindow.geometry("1400x800")
tkWindow.title('Weather For Sailors')

normal_font = font.Font(family="Arial", size=20)
bold_font = font.Font(family="Arial", size=24, weight="bold")

frame1 = Frame(tkWindow, bg="#0b419e", width=450, height=660)
frame1.place(x=10, y=100)

frame2 = Frame(tkWindow, bg="#2473d4", width=470, height=660)
frame2.place(x=470, y=100)

frame3 = Frame(tkWindow, bg="#40aadb", width=440, height=660)
frame3.place(x=949, y=100)

wind_speed, temperature = get_weather_conditions()
choice_wind_speed(wind_speed)
choice_tide_time()
choice_temperature(temperature)
condition_text = StringVar()
condition_text.set("")

title_label = Label(tkWindow, textvariable=condition_text, font=("Arial", 50))
title_label.place(relx=0.5, y=45, anchor=CENTER)

tkWindow.mainloop()
