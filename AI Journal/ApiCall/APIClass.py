#API AIzaSyAGQjDk_YJywo3mcL5ZsklXEr3nCat1FtQ

from datetime import datetime

from UserClass import User
from WeatherApi import WeatherAPI
from LocationApi import LocationApi

if __name__ == "__main__":
    address = '1200 Frank E Rodgers Blvd South, Harrison, NJ'
    user = User("Viraj","vv4389@gmail.com","+1 5855536727")

    location = LocationApi(user)
    lati, longi = location.get_lati_longi(address)
    weather = WeatherAPI(user).get_weather(lati,longi,datetime.now())
    print("Test LocationAPI")
    print(f"{user}")
    print(f"Address: {address}")
    print(f"Latitude: {lati}")
    print(f"Longitude: {longi}")
    print(f"Weather: {weather}")
