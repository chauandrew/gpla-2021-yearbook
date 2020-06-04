import pymongo
import os

# global UPLOAD_FOLDER
# global DBCLIENT

UPLOAD_FOLDER = f"/static/images/posts" # Post images

if 'PROD_ENV' in os.environ and os.environ['PROD_ENV']:
	# Production Settings
	client = pymongo.MongoClient("mongodb+srv://holynugget:KdYcnS5LWJgAchDI@cluster0-fuwyc.mongodb.net/test?retryWrites=true&w=majority")
	DBCLIENT = client["FlaskApp"]
	COMPRESSION_KEY = os.environ['TINYPNG_KEY']
else:
	# Local Settings
	
	# client = pymongo.MongoClient("localhost:27017") # Local
	
	client = pymongo.MongoClient("mongodb+srv://holynugget:KdYcnS5LWJgAchDI@cluster0-fuwyc.mongodb.net/test?retryWrites=true&w=majority")
	DBCLIENT = client["TestDb"] # use different collection under same cluster to test so we can share test data

	#file = f"{os.path.expanduser('~')}/.tinypng_key.txt"
	COMPRESSION_KEY = ""
	#with open(file, 'r') as file:
	#	COMPRESSION_KEY = file.read().replace('\n', '')