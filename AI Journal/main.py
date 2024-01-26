from UserClass import User
from LocationApi import LocationApi
from WeatherApi import WeatherAPI
from datetime import datetime
def main():
    print(f"Main Test")
    address = '286 E Squire Dr, Rochester, NY, USA'
    user = User("Viraj", "vv4389@gmail.com", "+1 5855536727")
    print(f"    UserClass: Success!")
    latitude, longitude  = LocationApi(user).get_lati_longi(address)
    print(f"    LocationAPI: Success!")
    weather = WeatherAPI(user).get_weather(latitude, longitude, datetime.now())
    print(f"    WeatherAPI: Success!")
    print(f"    Result:")
    print(f"        {user}")
    print(f"        Address: {address}")
    print(f"        Latitude: {latitude}")
    print(f"        Longitude: {longitude}")
    print(f"        Weather: {weather}")

if __name__ == "__main__":
    main()
