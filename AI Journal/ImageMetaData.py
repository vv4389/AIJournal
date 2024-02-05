from datetime import datetime

from PIL import Image, ExifTags
from dms2dec.dms_convert import dms2dec
import logging
from logging_config import configure_logging
from LocationApi import LocationApi
import streamlit as st

configure_logging()


class ImageMetaData:
    def __init__(self, st):
        self.__st = st

    def user_address(self):
        self.__st.subheader("Meta Data missing!!")
        address = self.__st.text_input("Please enter address where the image was taken: ")
        if address is not None:
            latitude, longitude = LocationApi().get_coordinates(address)
            if latitude is not None and longitude is not None:
                return latitude, longitude, address

    def user_date(self):
        date = self.__st.text_input("Please enter date when the image was taken (YYYY-MM-DD): ")
        if date is not None:
            return date

    def __GetMetaData(self, img):
        exif = None
        try:
            exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
        except Exception as e:
            logging.warning(f"MetaData Error: Meta data not present:\n{e}")
        return exif

    def __convert_to_date(self, time_str):
        date = None
        try:
            date = datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d")
        except Exception as e:
            logging.warning(f"Date conversion failed:\nInput:{time_str}\nError:{e}")
        return date

    def GetCoordinates(self, img):
        meta_data = {}
        exif = self.__GetMetaData(img)

        if exif is not None:
            Gps = exif.get('GPSInfo')
            if Gps:
                meta_data["latitude"] = dms2dec(f'''{str(Gps[2][0])}°{str(Gps[2][1])}'{str(Gps[2][2])}"{str(Gps[1])}''')
                meta_data["longitude"] = dms2dec(
                    f'''{str(Gps[4][0])}°{str(Gps[4][1])}'{str(Gps[4][2])}"{str(Gps[3])}''')
                meta_data["address"] = LocationApi().get_address(meta_data["latitude"], meta_data["longitude"])
            else:
                meta_data["latitude"], meta_data["longitude"], meta_data["address"] = self.user_address()

            date = exif.get('DateTime')

            if date:
                meta_data["date"] = self.__convert_to_date(date)
            else:
                meta_data["date"] = self.user_date()

        else:
            meta_data["latitude"], meta_data["longitude"], meta_data["address"] = self.user_address()
            meta_data["date"] = self.user_date()

        if meta_data.get("latitude") is not None and meta_data.get("longitude") is not None and meta_data.get(
                "date") is not None and meta_data.get("address"):
            return meta_data.get("latitude"), meta_data.get("longitude"), meta_data.get("date"), meta_data.get(
                "address")
        else:
            return None, None, None, None


if __name__ == "__main__":
    img = Image.open("/Users/virajvora/Downloads/IMG_7223.JPG")
    gps = ImageMetaData(st).GetCoordinates(img)
    print(gps)