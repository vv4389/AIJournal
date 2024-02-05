import os
import urllib.request
import sys
import json
import logging
from logging_config import configure_logging
import streamlit as st

configure_logging()


class WeatherApi:
    def __init__(self):
        self.__weather_api = os.environ.get("VCWeatherApiKey")

    @st.cache_resource(show_spinner=False)
    def get_weather_data(_self, location, date):
        jsonData = None
        if location[0] is not None and location[1] is not None and date is not None and len(date) > 1:
            try:
                ResultBytes = urllib.request.urlopen(
                    f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location[0]}%2C%20{location[1]}/{date}/{date}?unitGroup=us&elements=datetime%2Ctemp%2Cfeelslike%2Chumidity%2Cprecip%2Cpreciptype%2Cwindspeed&include=days&key={_self.__weather_api}&contentType=json")

                # Parse the results as JSON
                jsonData = json.load(ResultBytes)

            except urllib.error.HTTPError as e:
                ErrorInfo = e.read().decode()
                logging.warning('VisualCrossing Weather Api Error:\nError code: ', e.code, ErrorInfo)
                sys.exit()
            except urllib.error.URLError as e:
                ErrorInfo = e.read().decode()
                logging.warning('VisualCrossing Weather Api Error:\nError code: ', e.code, ErrorInfo)
                sys.exit()

            if jsonData is not None:
                return jsonData["days"][0]
            else:
                return None


if __name__ == "__main__":
    weather = WeatherApi()
    print(weather.get_weather_data((4.55678, 5.5759), "2023-12-20"))
