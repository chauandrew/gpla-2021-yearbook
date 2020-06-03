import pymongo
import os

# global UPLOAD_FOLDER
# global DBCLIENT

# Local Settings
# UPLOAD_FOLDER = '{os.path.expanduser('~')}/testing' # Local
# client = pymongo.MongoClient("127.0.0.1:27017") # Local

# Production Settings
UPLOAD_FOLDER = f"{os.path.expanduser('~')}/image-data"
client = pymongo.MongoClient("mongodb+srv://holynugget:KdYcnS5LWJgAchDI@cluster0-fuwyc.mongodb.net/test?retryWrites=true&w=majority")

DBCLIENT = client["FlaskApp"]
