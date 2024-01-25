#API AIzaSyAGQjDk_YJywo3mcL5ZsklXEr3nCat1FtQ

from datetime import datetime

from UserClass import User
from WeatherApi import WeatherAPI
from LocationApi import LocationApi

if __name__ == "__main__":
    address = '286 E Squire Dr, Rochester, NY, USA'
    user = User("Viraj","vv4389@gmail.com","+1 5855536727")

    location = LocationApi(user)
    lati, longi = location.get_lati_longi(address)
    weather = WeatherAPI(user)
    print("Test LocationAPI")
    print(f"Latitude: {lati}")
    print(f"Longitude: {longi}\n\n\n")

    print(weather.get_weather(lati,longi,datetime.now()))
