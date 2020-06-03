import pymongo
import os

# global UPLOAD_FOLDER
# global DBCLIENT

# Local Settings
# UPLOAD_FOLDER = f"{os.path.expanduser('~')}/testing" # Local
# client = pymongo.MongoClient("127.0.0.1:27017") # Local
# file = f"{os.path.expanduser('~')}/.tinypng_key.txt"
# COMPRESSION_KEY = ""
# with open(file, 'r') as file:
#     COMPRESSION_KEY = file.read().replace('\n', '')

# Production Settings
UPLOAD_FOLDER = f"{os.path.expanduser('~')}/image-data"
client = pymongo.MongoClient("mongodb+srv://holynugget:KdYcnS5LWJgAchDI@cluster0-fuwyc.mongodb.net/test?retryWrites=true&w=majority")
COMPRESSION_KEY = os.environ['TINYPNG_KEY']

DBCLIENT = client["FlaskApp"]