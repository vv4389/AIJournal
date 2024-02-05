from datetime import datetime

from PIL import Image, ExifTags
from dms2dec.dms_convert import dms2dec
import logging
from logging_config import configure_logging
from LocationApi import LocationApi
import streamlit as st

configure_logging()


class ImageMetaData:

    def user_input(self):

        placeholder = st.empty()
        with placeholder.form("user input"):
            st.subheader("Meta Data missing!!")

            address = st.text_input("Please enter address where the image was taken: ")
            date_input = st.date_input("Please enter date when the image was taken (YYYY-MM-DD): ")

            submitted = st.form_submit_button()

        if submitted:

            # Format the selected date to "YYYY-MM-DD"
            formatted_date = date_input.strftime("%Y-%m-%d")
            latitude, longitude = LocationApi().get_coordinates(address)
            placeholder.empty()
            return latitude, longitude, address, formatted_date
        else:
            return None, None, None, None

    def __GetMetaData(self, img):
        exif = None
        try:
            exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
        except Exception as e:
            logging.warning(f"MetaData Error: Meta data not present:\n{e}")
        return exif

    def __convert_to_date(self, time_str: str):
        date = None
        try:
            date = datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d")
        except Exception as e:
            logging.warning(f"Date conversion failed:\nInput:{time_str}\nError:{e}")
        return date

    def __convert_to_coords(self, Gps, direction):
        return dms2dec(f'''{str(Gps[0])}°{str(Gps[1])}'{str(Gps[2])}"{str(direction)}''')

    def GetCoordinates(self, img):
        meta_data = {}
        exif = self.__GetMetaData(img)

        if exif is not None:
            Gps = exif.get('GPSInfo')
            date = exif.get('DateTime')

            if Gps and date:
                meta_data["latitude"] = self.__convert_to_coords(Gps[2], Gps[1])
                meta_data["longitude"] = self.__convert_to_coords(Gps[4], Gps[3])
                meta_data["address"] = LocationApi().get_address(meta_data["latitude"], meta_data["longitude"])
                meta_data["date"] = self.__convert_to_date(date)

            else:
                meta_data["latitude"], meta_data["longitude"], meta_data["address"], meta_data[
                    "date"] = self.user_input()
        else:
            meta_data["latitude"], meta_data["longitude"], meta_data["address"], meta_data[
                "date"] = self.user_input()
        return meta_data.get("latitude"), meta_data.get("longitude"), \
            meta_data.get("date"), meta_data.get("address")


if __name__ == "__main__":
    img = Image.open("/Users/virajvora/Downloads/IMG_7223.JPG")
    gps = ImageMetaData().GetCoordinates(img)
    print(gps)
