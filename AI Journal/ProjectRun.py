import logging
import time
from datetime import datetime

import streamlit as st
from PIL import Image

from ImageMetaData import ImageMetaData
from LlmModel import process_image_with_weather
from UserClass import User
from VCWeatherApi import WeatherApi
from logging_config import configure_logging
from GCPStorageManagement import StorageManagement

configure_logging()
testing = False


class ProjectRun:
    def __init__(self, user, img, st):
        self.__storage_management = StorageManagement()
        self.user = user
        self.img = img
        self.st = st

    def SystemRun(self):
        logging.info(f"Main.py: {datetime.utcnow()}")
        if self.img:
            latitude, longitude, date, address = ImageMetaData(st).GetCoordinates(self.img)
            if latitude is not None and longitude is not None and date is not None and address is not None:
                weather = WeatherApi().get_weather_data((latitude, longitude), date)
                print(weather)
                if weather is not None:
                    time.sleep(1)
                    if testing:
                        print(f"    Result:")
                        print(f"        {self.user}")
                        print(f"    1234    Address: {address}")
                        print(f"        Latitude: {latitude}")
                        print(f"        Longitude: {longitude}")
                        print(f"        Weather: {weather}")
                    img_url = self.__storage_management.create_uri(_user=self.user, _img=self.img)
                    if address is not None and len(address) > 3:
                        print(f"Address: {address}")
                        output_data = f"        Summary: {process_image_with_weather(image_url=img_url, address=address, weather_data=weather)}"
                        self.__storage_management.blob_make_private(_user=self.user)
                        self.__storage_management.delete_blob(_user=self.user)
                        return output_data
        else:
            st.write("Image not Found!!!")


if __name__ == "__main__":
    import SetupEnv
    testing = True
    SetupEnv.setup()
    img = Image.open("IMG_7223.JPG")
    print(ProjectRun(User(img), img, st).SystemRun())