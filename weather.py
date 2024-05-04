#!/usr/bin/env python
'''
Name:    Sheldon Codling
CNumber: C0596137
'''

from tkinter.constants import CENTER
import requests
import tkinter as tk
import time
from PIL import ImageTk, Image

def get_weather(city):
    global img
    #API key
    #api_key = "9fd3b28a908bfc08ebc58be022ef5395"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=9fd3b28a908bfc08ebc58be022ef5395"
    response = requests.get(url).json()

    # Weather variables
    weatherDesc = response["weather"][0]["main"]

    # Temperature variables
    tempC = "{0:.1f}".format(response["main"]["temp"] - 273.15) + "°C" # Convert to celsius
    tempF = "{0:.1f}".format((response["main"]["temp"] * 1.8) - 459.67) + "°F" #Convert to fahrenheit
    
    # Wind variables
    windSpeed = response["wind"]["speed"]

    # Humidity variables
    humidity = response["main"]["humidity"]

    # Sunrise/sunset variables
    sunRise = time.strftime("%I:%M %p", time.gmtime(response["sys"]["sunrise"] + response["timezone"]))
    sunSet = time.strftime("%I:%M %p", time.gmtime(response["sys"]["sunset"] + response["timezone"]))

    # Return the information
    #return userCity, weatherDesc, weatherIconFileName, tempC, tempF, sunRise, sunSet
    cityLabel.config(text = response["name"])
    weatherLabel.config(text = weatherDesc)
    tempLabel.config(text = tempC + " | " + tempF)
    feelsLabel.config(text = "Feels like: " + "{0:.1f}".format(response["main"]["feels_like"] +  - 273.15) + "°C")
    windSpeedLabel.config(text = "Wind Speed:   " + str(response["wind"]["speed"]) + "m/s")
    humidityLabel.config(text = "Humidity:   " + str(humidity) + "%")
    sunriseLabel.config(text = "Sunrise:   " + str(sunRise))
    sunsetLabel.config(text = "Sunset:   " + str(sunSet))

    # Get the correct icon for the weather
    imgUrl = response["weather"][0]["icon"]
    img = ImageTk.PhotoImage(file = f"images/{imgUrl}@2x.png")
    iconLabel.config(image = img)
    
def updateClock(timeLeft):
    timeLeft -= 1

    timerLabel.config(text = "Next update: " + time.strftime("%M:%S", time.gmtime(timeLeft)))
    timerLabel.after(1000, lambda: updateClock(timeLeft))

    if timeLeft == 0:
        timeLeft = 15
        get_weather(currentCity)

def updateCity():
    global currentCity, cityEntry

    currentCity = cityEntry.get()
    get_weather(currentCity)

if __name__ == "__main__":
    #tkinter set up
    root = tk.Tk()
    root.configure(background="#8FE2FF")
    root.attributes('-fullscreen', True)
    root.title("Sheldon's weather app")
    root.geometry("500x600")
    root.minsize(500, 600)
    # Frames
    top = tk.Frame(root, bg="#8FE2FF")
    middle = tk.Frame(root, bg="#8FE2FF")
    bottom = tk.Frame(root, bg="#000000")
    
    # City
    currentCity = "Sarnia,CA"
    # 30 minute timer
    timeTilUpdate = 1800

    # center everything
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Top frame
    entryLabel = tk.Label(top, text="Enter your city: ", font=("Helvetica, 24"), bg="#8FE2FF")
    cityEntry = tk.Entry(top, width = 10, font=("Helvetica, 24"))
    updateButton = tk.Button(top, text = "update", pady = 3, command = updateCity, font=("Helvetica, 14 bold"), bg="#A20202", fg="#FFFFFF")
    # Middle frame
    cityLabel = tk.Label(middle, text = "", font=("Helvetica, 28 bold"), bg="#8FE2FF")
    tempLabel = tk.Label(middle, text = "", font=("Helvetica, 32 bold"), bg="#8FE2FF")
    feelsLabel = tk.Label(middle, text = "", font=("Helvetica, 24"), bg="#8FE2FF")
    iconLabel = tk.Label(middle, width = 100, height = 100, bg="#8FE2FF")
    weatherLabel = tk.Label(middle, text = "", font=("Helvetica, 24"), bg="#8FE2FF")
    windSpeedLabel = tk.Label(middle, text = "", font=("Helvetica, 24"), bg="#8FE2FF")
    humidityLabel = tk.Label(middle, text = "", font=("Helvetica, 24"), bg="#8FE2FF")
    sunriseLabel = tk.Label(middle, text = "", font=("Helvetica, 24"), bg="#8FE2FF")
    sunsetLabel = tk.Label(middle, text = "", font=("Helvetica, 24"), bg="#8FE2FF")
    # Bottom Frame
    timerLabel = tk.Label(bottom, text = "", font=("Helvetica, 16"), bg="#1c1c1c", fg="#ffffff")

    # Set all the widgets to use the grid placement system
    top.grid()
    middle.grid()
    bottom.grid()
    entryLabel.grid(row=0, column=0)
    cityEntry.grid(row=0, column=1)
    updateButton.grid(row = 0, column = 2)
    cityLabel.grid()
    iconLabel.grid()
    weatherLabel.grid()
    tempLabel.grid()
    feelsLabel.grid()
    windSpeedLabel.grid()
    humidityLabel.grid()
    sunriseLabel.grid()
    sunsetLabel.grid()
    timerLabel.grid()

    updateClock(timeTilUpdate) # Start the countdown clock
    get_weather(currentCity) # Get the initial data

    root.mainloop()