# This program will connect to the OpenWeather API, and provide weather information on location
import requests
import json
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox

# Creation of the Weather_Api class. This has the api_key that will be used to request information from the API
class Weather_Api:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    # The geocoder built into the weathermap weather API is outdated, so need to get city information from their geocoding API
    def get_city(self, city):
        city_url = "http://api.openweathermap.org/geo/1.0/direct?"
        params = {"q": city, "limit": 1, "appid": self.api_key}
        
        # This returns the latitude and longitude of the city, which is then used for the weather API
        response = requests.get(city_url, params=params)
        if response.status_code == 200:
            city_data = response.json()
            if city_data:
                lat = city_data[0]["lat"]
                lon = city_data[0]["lon"]
                return lat, lon
            else:
                sys.exit("No info found on city")
                
        else:
            sys.exit(f"Error: {response.status_code}")
      
    # This is the function that will get the weather information, for the lat and lon found in get_city
    def get_weather(self, city_lat, city_lon):
        params = {"lat": city_lat, "lon": city_lon, "appid": self.api_key}
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            sys.exit(f"Error: {response.status_code}")

def show_weather():
    # Creating a tkinter window for the input, rather than typing into terminal
    root = tk.Tk()
    root.title("Weather Information")
    output_text = tk.Text(root, wrap=tk.WORD, width=40, height=10)
    output_text.pack(padx=10, pady=10)
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    
    # Provide API key, then ask for an input city
    api_key = "INSERT API KEY HERE https://home.openweathermap.org/api_keys"
    weather_api = Weather_Api(api_key)
    city_name = simpledialog.askstring("Input", "Please input the name of a city: ")

    if city_name:
        # This retrieves the latitude and longitude, and store in city_lat, city_lon
        city_lat, city_lon = weather_api.get_city(city_name)
        #print(f"Latitude: {city_lat}")
        #print(f"Longitude: {city_lon}")

        if city_lat and city_lon:
        # This get the weather information using the lat and lon from get_city, then formats below
            city_weather = weather_api.get_weather(city_lat, city_lon)
            if city_weather:
                weather_main = city_weather["weather"][0]["main"]
                #weather_description = city_weather["weather"][0]["description"]
                weather_temp = city_weather["main"]["temp"]
                output_text.insert(tk.END, f"Weather Condition: {weather_main}\n")
                output_text.insert(tk.END, f"Temp: {round((weather_temp - 273.15), 0)} degrees celsius")
            else:
                messagebox.showerror("Error", "Failed to fetch weather data.")
        else:
            messagebox.showerror("Error", "Failed to fetch city location.")
    else:
        messagebox.showerror("Error", "Invalid city input.")
    root.mainloop()
        #print(json.dumps(city_weather, indent=4))
        #print(f"The weather in {city_name} is currently {weather_main} with {weather_description}. It is currently {round((weather_temp - 273.15), 0)} degrees celsius")
show_weather()