#API AIzaSyAGQjDk_YJywo3mcL5ZsklXEr3nCat1FtQ
import requests
from UserClass import User

class LocationApi:
    def __init__(self, user:User, google_Api='AIzaSyAGQjDk_YJywo3mcL5ZsklXEr3nCat1FtQ'):
        self.user = user
        self.__google_api = google_Api


    def __get_lati_longi__(self, address):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'

        params = {

            "address": address,

            "key": self.__google_api

        }

        response = requests.get(url, params=params)

        if response.status_code == 200:

            data = response.json()

            if data["status"] == "OK":

                location = data["results"][0]["geometry"]["location"]

                lat = location["lat"]

                lng = location["lng"]

                return lat, lng

            else:

                print(f"Error: {data['error_message']}")

                return 0, 0

        else:

            print("Failed to make the request.")

            return 0, 0

    def get_lati_longi(self, address):
        return self.__get_lati_longi__(address)

if __name__ == "__main__":
    address = '286 E Squire Dr, Rochester, NY, USA'
    user = User("Viraj","vv4389@gmail.com","+1 5855536727")

    location = LocationApi(user)
    lati, longi = location.get_lati_longi(address)
    print("Test LocationAPI")
    print(f"Latitude: {lati}")

    print(f"Longitude: {longi}")