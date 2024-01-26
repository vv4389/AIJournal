from datetime import datetime

import requests

from UserClass import User
from LocationApi import LocationApi
class WeatherAPI:
    def __init__(self, user:User, weather_Api='1OwOEbF9KD4XBisiewEdGgEMhrpsI01v'):
        self.user = user
        self.__weather_api = weather_Api

    def __get_weather(self, latitude, longitude,timestamp):
        default_precipitation = {"1": "Rain","2": "Snow","3": "Freezing Rain","4": "Ice Pellets / Sleet"}
        startTime = self.__get_formatted_timestamp(timestamp,-6)
        endTime = self.__get_formatted_timestamp(timestamp,6)
        timestamp = self.__get_formatted_timestamp(timestamp,0)
        # weather_url =  f'https://api.tomorrow.io/v4/timelines?location={latitude},{longitude}&fields=temperature,humidity,windspeed&timesteps=1h&startTime={startTime}&endTime={endTime}&units=metric&apikey={self.__weather_api}'
        weather_url =  f'https://api.tomorrow.io/v4/timelines?location={latitude},{longitude}&fields=temperature,humidity,windSpeed,precipitationIntensity,precipitationType&timesteps=30m&startTime={startTime}&endTime={endTime}&units=metric&apikey={self.__weather_api}'
        print(weather_url)
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                # Extracting interval columns
                weather_dict = {}
                # print(data["data"]["timelines"][0])
                precipitation = dict()
                for interval in data["data"]["timelines"][0]["intervals"]:
                    start_time = interval["startTime"]
                    humidity = interval["values"]["humidity"]
                    windspeed = interval["values"]["windSpeed"]
                    temperature = interval["values"]["temperature"]
                    precipitation_type = str(interval["values"].get("precipitationType"))

                    if precipitation_type is not None:
                        if precipitation_type in precipitation:
                            precipitation[precipitation_type] = precipitation[precipitation_type] + float(interval["values"]["precipitationIntensity"])
                            # precipitation[precipitation_type] += float(interval["values"]["precipitationIntensity"])
                        else:
                            precipitation[precipitation_type] = float(interval["values"]["precipitationIntensity"])

                    else:
                        # Handle the case when 'precipitationType' key is not present
                        print("Key 'precipitationType' not found in the dictionary.")
                    # precipitation[interval["values"]["precipitationType"]] += float(interval["values"]["precipitationIntensity"])

                    weather_dict[start_time] = dict(humidity=humidity, temperature=temperature,windspeed=windspeed)

                avg_precipitation = {}
                total_weather_data = len(weather_dict)
                for key,value in precipitation.items():
                    avg_precipitation[default_precipitation[key]] = value/total_weather_data


                required_weather_data = {
                    'timestamp': timestamp,
                    'avg_precipitation':avg_precipitation
                }
                for key,value in weather_dict[timestamp].items():
                    required_weather_data[key] = value

                return required_weather_data
            else:
                print(f"Error: {data['error_message']}")
                return 0, 0
        else:
            print("Failed to make the request.\n",response)
            return 0, 0

    def get_weather(self, latitude, longitude, timestamp=datetime.now()):
        return self.__get_weather(latitude, longitude, timestamp)

    @staticmethod
    def __get_formatted_timestamp(currentDate, addHours):
        if currentDate.hour + addHours<24:
            hrs = currentDate.hour + addHours
            timestamp = "{0}T{1}:{2}:{3}Z".format(str(currentDate.date()), f"{hrs:02d}",
                                              f"00", f"00")
        else:
            timestamp = "{0}T{1}:{2}:{3}Z".format(str(currentDate.date()), f"24",
                                             f"59", f"59")
        return timestamp

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
