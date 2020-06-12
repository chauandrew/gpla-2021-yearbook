from config import DBCLIENT, UPLOAD_FOLDER, COMPRESSION_KEY
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET

from flask import request, jsonify, render_template, make_response, Blueprint
import pymongo
from werkzeug.utils import secure_filename
import tinify # for compression api
import boto3

import os
from pathlib import Path
import re
import datetime
import json
from bson import ObjectId
import threading
from time import sleep

timeline = Blueprint('timeline', __name__)
tinify.key = COMPRESSION_KEY
s3_client = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.gif']
COMPRESSABLE_EXTENSIONS = ['.jpg', '.png', '.jpeg']
TO_UPLOAD = []
SLEEP_TIME = 5

# Turn single length arrays into standalone objects
def parse_input(args):
    for k, v in args.items():
        if isinstance(v, list) and len(v) == 1:
            args[k] = v[0]
        if args[k] == "":
            del args[k]
    return args


@timeline.route("/api/timeline/upload", methods=['POST'])
def upload_event():
    # Parse arguments
    args = request.form.to_dict(flat=False)
    args = parse_input(args)
    print(f"Received {args}")
    files = request.files.getlist("file")
    files = [file for file in files if file.filename != ''] # filter
    if 'date' not in args:
        return "'date' field is required"
    elif not re.match("^(19|20)\d\d-(0|1)\d-[0-3]\d$", str(args['date'])):
        return make_response("date must be valid and look like: 'YYYY-MM-DD'", 400)
    if 'body' not in args or args['body'] == "":
        return make_response("Description field is required!", 400)
    if 'title' not in args:
        return make_response("Event must have a 'title'.",400)
    for file in files:
        _, ext = os.path.splitext(file.filename)
        if ext.lower() not in ALLOWED_EXTENSIONS:
            return make_response("File must be .gif, .jpg, .jpeg, or .png", 400)
    if len(files) == 0:
        return make_response("Event must have at least one photo", 400)
    # Write images into local filesystem
    now = str(datetime.datetime.now()).replace(' ','')
    dirname = os.path.dirname(os.path.realpath(__file__))
    upload_folder = f"{UPLOAD_FOLDER}/timeline/{now}"
    Path(dirname + upload_folder).mkdir(parents=True, exist_ok=True)
    for file in files:
        filename = secure_filename(file.filename)
        file.save(f"{dirname}{upload_folder}/{filename}")

    # Queue images to be uploaded by background task
    TO_UPLOAD.append({'args': args, 'files': files, 'timestamp': now})
    return make_response("Upload successfully queued!", 200)

    return json.dumps({}, default=str)

# Thread running in background to compress images and then upload to s3
def background_timeline_upload():
    global TO_UPLOAD
    while True:
        sleep(SLEEP_TIME)
        try:
            i = 0
            for request in TO_UPLOAD:
                args = request['args']
                files = request['files']
                print(files)
                now = request['timestamp']
                paths = []
                dirname = os.path.dirname(os.path.realpath(__file__)) 
                upload_folder = f"{UPLOAD_FOLDER}/timeline/{now}"
                # Save files locally, compress, upload to s3, delete locally
                for file in files:
                    filename = secure_filename(file.filename)
                    path = f"{dirname}{upload_folder}/{filename}"  # path on server
                    object_name = f"timeline/{now}/{filename}"     # object name on s3

                    # compress for compatible file types
                    ext = filename.split('.')[-1]
                    if ext.lower() in COMPRESSABLE_EXTENSIONS:
                        source = tinify.from_file(path) # compress
                        source.to_file(path)

                    s3_client.upload_file(path, S3_BUCKET, object_name) # upload to s3
                    os.remove(path) # remove from local filesystem
                    paths.append(object_name)

                args['files'] = paths # 'files' stores paths of s3 objects
                args['comments'] = []
                print(args)
                # Upload to database and return
                result = DBCLIENT['Timeline'].insert_one(args)
                i += 1
            TO_UPLOAD = TO_UPLOAD[i:] # Remove the number of elements we processed
        except Exception as e:
            print(e)
            pass


@timeline.route("/api/timeline/get", methods=['POST'])
def get_events():
    cursor = DBCLIENT['Timeline'].find()
        # For each image, get presigned url and replace filepath with that
    response = []
    for doc in cursor:
        buckets = []
        for file in doc['files']:
            url = s3_client.generate_presigned_url('get_object', 
                Params={'Bucket':S3_BUCKET, 'Key': file},
                ExpiresIn=3600
            )
            buckets.append(url)
        doc['files'] = buckets
        response.append(doc)
    return json.dumps(response, default=str)

bkgd_upload = threading.Thread(name='upload', target=background_timeline_upload)
bkgd_upload.start()