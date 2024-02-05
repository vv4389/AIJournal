import logging
from logging_config import configure_logging
from PIL import Image
from UserClass import User
import streamlit as st

try:
    import os
    from google.cloud import storage
    from datetime import datetime, timedelta
    import json
except Exception as e:
    logging.warning(f"Error importing modules in StorageApi:\n{e}")

configure_logging()


class StorageManagement:

    def __init__(self):
        self.__bucket_name = os.environ.get("storage_bucket_name")
        try:
            json_data_str = os.environ.get("gcp_credentials")
            print(json_data_str)
            json_data = json.loads(json_data_str)
            self.__storage_client = storage.Client.from_service_account_info(json_data)
        except Exception as e:
            logging.warning(f"GCP connection failed:\n{e}")
        self.__bucket = self.__storage_client.bucket(self.__bucket_name)
        self.__blobs = {}

    class Blob:
        def __init__(self, bucket, blob_name):
            self.blob_name = blob_name
            self.__bucket = bucket
            self.__blob = self.__bucket.blob(self.blob_name)

        def get_blob(self):
            return self.__bucket.blob(self.blob_name)

        def delete_blob(self):
            self.__blob.delete()

        def delete(self):
            self.__blob.delete()

    @st.cache_resource(show_spinner=False)
    def __upload_file_to_cloud_storage(_self, _blob, local_file_path, destination):
        """Uploads a file to Google Cloud Storage."""
        try:
            _blob.get_blob().upload_from_filename(local_file_path)
            logging.info(f"File {local_file_path} uploaded to {destination}.")
        except Exception as e:
            logging.warning(f"GCP UPLOAD FAILED!:\n{e}")

    @st.cache_resource(show_spinner=False)
    def __make_file_public(_self, _blob: Blob):
        """Makes the image object in Cloud Storage public."""
        try:
            _blob.get_blob().make_public()
            logging.info(f"Blob {_blob.blob_name} is now publicly accessible.")
        except Exception as e:
            logging.warning(f"GCP PUBLIC FAILED!:\n{e}")

    def __get_image_uri(_self, blob):
        """Gets the public URI of the image in Cloud Storage."""
        return f"https://storage.googleapis.com/{_self.__bucket_name}/{blob.blob_name}"

    @st.cache_resource(show_spinner=False)
    def blob_make_private(_self, _user):
        if _user.uid in _self.__blobs:
            try:
                blob = _self.__blobs[_user.uid].get_blob()
                blob.acl.all().revoke_read()
                blob.acl.save(client=blob.client)
                logging.info(f"Blob {_self.__blobs[_user.uid].blob_name} is now privately accessible.")

            except Exception as e:
                logging.warning(f"Blob Error: Privatization error!! \n{e}")

    @st.cache_resource(show_spinner=False)
    def create_uri(_self, _user, _img):
        destination = '{0}{1}.JPG'.format(os.environ.get('destination_blob_path'), str(_user.uid))
        if _user.uid not in _self.__blobs:
            _self.__blobs[_user.uid] = _self.Blob(_self.__bucket, destination)

        local_file_path = str(_user.uid) + ".JPG"
        _img.save(local_file_path)
        # Upload image to Cloud Storage
        blob_object = _self.__blobs[_user.uid]
        _self.__upload_file_to_cloud_storage(blob_object, local_file_path=local_file_path, destination=destination)
        os.remove(local_file_path)
        # Make the image public
        _self.__make_file_public(blob_object)

        # Get the public URI
        uri = _self.__get_image_uri(blob_object)

        return uri

    def close(self):
        try:
            self.__storage_client.close()
        except Exception as e:
            logging.warning(f"GCP CLIENT CLOSE ERROR!:\n{e}")

    @st.cache_resource(show_spinner=False)
    def delete_blob(_self, _user):
        if _user.uid in _self.__blobs:
            try:
                _self.__blobs[_user.uid].delete()
                del _self.__blobs[_user.uid]
            except Exception as e:
                logging.warning(f"Blob Error: deletion error!! \n{e}")
        else:
            try:
                blob = _self.__bucket.get_blob(_user.uid)
                if blob is not None:
                    blob.delete()
            except Exception as e:
                logging.warning(f"Blob Error: Blob not found!!\n{e}")


if __name__ == "__main__":
    import SetupEnv

    SetupEnv.setup()
    local_file = "FamilyCamping-2021-GettyImages-948512452-2.webp"
    img = Image.open(local_file)
    username = User(img)
    blob1 = StorageManagement()
    print(blob1.create_uri(username, img=img))
    blob1.blob_make_private(user=username)
    blob1.delete_blob(user=username)
