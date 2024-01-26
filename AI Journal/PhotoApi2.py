from gphotospy import authorize
from gphotospy.album import *
CLIENT_SECRET_FILE = "token-for-google.json"
service = authorize.init(CLIENT_SECRET_FILE)
album_manager = Album(service)