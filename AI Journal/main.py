from CustomClass.UserClass import User
from ApiCall.LocationApi import LocationApi
from ApiCall.WeatherApi import WeatherAPI
from datetime import datetime
def main():
    print("Main Test")
    user = User("Viraj", "vv4389@gmail.com", "5855536727")
    location = LocationApi(user)
    address = '286 E Squire Dr, Rochester, NY, USA'
    print(f'Address: {address}')
    lat, longi = location.get_lati_longi(address)
    print(f'latitude: {lat}, Longitude: {longi}')
    weather = WeatherAPI(user)
    print(weather.get_weather(lat, longi, datetime.now()))

if __name__ == "__main__":
    main()