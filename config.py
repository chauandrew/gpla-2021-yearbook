import pymongo
import os

# global UPLOAD_FOLDER
# global DBCLIENT
# global DEBUG

UPLOAD_FOLDER = f"/static/images/" # Post images
S3_BUCKET = "staff-appreciation"
client = pymongo.MongoClient("mongodb+srv://holynugget:KdYcnS5LWJgAchDI@cluster0-fuwyc.mongodb.net/test?retryWrites=true&w=majority")

if 'PROD_ENV' in os.environ and os.environ['PROD_ENV']:
	# Production Settings
	AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
	AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
	DBCLIENT = client["FlaskApp"]
	COMPRESSION_KEY = os.environ['TINYPNG_KEY']
	DEBUG = False
else:
	# Local Settings
	DBCLIENT = client["TestDb"] # use different collection under same cluster to test so we can share test data
	AWS_ACCESS_KEY_ID = ""
	AWS_SECRET_ACCESS_KEY = ""
	COMPRESSION_KEY = ""
	DEBUG = True
