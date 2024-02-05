import os

import requests
import logging
from logging_config import configure_logging
import streamlit as st


class LocationApi:
    configure_logging()

    def __init__(self):
        self.__google_api = os.environ.get("google_Api_Key")

    @st.cache_resource(show_spinner=False)
    def __get_coordinates(_self, address):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'

        params = {
            "address": address,
            "key": _self.__google_api
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
                logging.warning(f"Location API Error:\n{data['error_message']}")
                return 0, 0

        else:

            logging.warning("Location API Error: Failed to make the request.")
            return 0, 0

    @st.cache_resource(show_spinner=False)
    def get_coordinates(_self, address):
        return _self.__get_coordinates(address)

    @st.cache_resource(show_spinner=False)
    def get_address(_self, latitude, longitude):
        # Google Maps Geocoding API endpoint
        api_endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

        # Prepare parameters for the API request
        params = {
            'latlng': f'{latitude},{longitude}',
            'key': _self.__google_api,
        }

        # Make the API request
        response = requests.get(api_endpoint, params=params)
        result = response.json()

        # Check if the request was successful
        if response.status_code == 200 and result['status'] == 'OK':
            # Extract the formatted address from the first result
            formatted_address = result['results'][0]['formatted_address']
            return formatted_address
        else:
            logging.warning(f"LocationApi error: get_address failed: {latitude}, {longitude} :\n{response.json()}")
            return None


if __name__ == "__main__":
    test_address = '286 E Squire Dr, Rochester, NY, USA'
    lati, longi = LocationApi().get_coordinates(test_address)
    new_address = LocationApi().get_address(lati, longi)
    print("Test LocationAPI")
    print(f"Latitude: {lati}")
    print(f"Longitude: {longi}")
    print(f"fetched Address: {new_address}")