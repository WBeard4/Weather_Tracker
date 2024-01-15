# This program will connect to the OpenWeather API, and provide weather information on location (currently only London)
import requests

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
                print("No info found on city")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
        
api_key = "INSERT API KEY HERE"
weather_api = Weather_Api(api_key)
city_name = input("Please input the name of a city: ")
city_lat_lon = weather_api.get_city(city_name)
if city_lat_lon:
    print(f"Latitude: {city_lat_lon[0]}")
    print(f"Longitude: {city_lat_lon[1]}")
