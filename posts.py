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

posts = Blueprint('posts', __name__)

PAGE_SIZE=3
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.gif']
COMPRESSABLE_EXTENSIONS = ['.jpg', '.png', '.jpeg']
TO_UPLOAD = []
SLEEP_TIME = 3 # seconds for background upload thread to sleep
tinify.key = COMPRESSION_KEY
s3_client = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Turn single length arrays into standalone objects
def parse_input(args):
    for k, v in args.items():
        if isinstance(v, list) and len(v) == 1:
            args[k] = v[0]
    return args

# Queue a post to be uploaded: needs: 'date', 'quarter', and ('files' or 'author','body')
@posts.route("/api/posts/upload", methods=['POST'])
def upload():
    # Parse arguments
    args = request.form.to_dict(flat=False)
    args = parse_input(args)
    files = request.files.getlist("file")
    files = [file for file in files if file.filename != ''] # filter
    if 'date' not in args:
        return "'date' field is required"
    elif not re.match("^(19|20)\d\d-(0|1)\d-[0-3]\d$", str(args['date'])):
        return make_response("date must be valid and look like: 'YYYY-MM-DD'", 400)
    if len(files) == 0:
        for key in ['author', 'body']:
            if args[key] == "":
                return make_response("Post without files must specify an 'author' and 'body'", 400)
        args['type'] = 'SHARING'
    elif len(files) > 1:
        if 'title' not in args:
            return make_response("Post with multiple files must specify a 'title'.",400)
        args['type'] = "ALBUM"
    else:
        args['type'] = "PHOTO"
    for file in files:
        _, ext = os.path.splitext(file.filename)
        if ext.lower() not in ALLOWED_EXTENSIONS:
            return make_response("File must be .jpg, .jpeg, or .png", 400)

    # Write images into local filesystem
    now = str(datetime.datetime.now()).replace(' ','')
    dirname = os.path.dirname(os.path.realpath(__file__))
    upload_folder = f"{UPLOAD_FOLDER}/posts/{now}"
    Path(dirname + upload_folder).mkdir(parents=True, exist_ok=True)
    print(files)
    for file in files:
        filename = secure_filename(file.filename)
        file.save(f"{dirname}{upload_folder}/{filename}")

    # Queue images to be uploaded by background task
    TO_UPLOAD.append({'args': args, 'files': files, 'timestamp': now})
    return make_response("Upload successfully queued!", 200)

# Thread running in background to compress images and then upload to s3
def background_post_upload():
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
                upload_folder = f"{UPLOAD_FOLDER}/posts/{now}"
                # Save files locally, compress, upload to s3, delete locally
                for file in files:
                    filename = secure_filename(file.filename)
                    path = f"{dirname}{upload_folder}/{filename}"  # path on server
                    object_name = f"posts/{now}/{filename}"        # object name on s3
                    
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
                result = DBCLIENT['Posts'].insert_one(args)
                i += 1
            TO_UPLOAD = TO_UPLOAD[i:] # Remove the number of elements we processed
        except Exception as e:
            print(e)
            pass


# Finds posts in a given quarter, sorted / paginated by date
@posts.route('/api/posts/<quarter>', methods=['POST'])
def find_by_quarter(quarter):
    if quarter.lower() not in ['summer','fall', 'winter', 'spring']:
        return make_response("quarter must be 'summer', 'fall', 'winter', or 'spring'", 400)
    args = request.form.to_dict(flat=False)
    # turn single length arrays into standalone objects, etc.
    args = parse_input(args)
    cursor = DBCLIENT['Posts'].find({'quarter': quarter.upper()})
    cursor.sort('date', pymongo.ASCENDING)
    response = []
    # For each image, get presigned url and replace filepath with that
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
    if 'page' in args:
        front = int(args['page']) * PAGE_SIZE
        return json.dumps(response[front:front+PAGE_SIZE], default=str)
    else:
        return json.dumps(response, default=str)


# Removes a post from mongodb using any available criteria to match
@posts.route("/api/posts/remove", methods=['POST'])
def remove():
    # Parse arguments
    args = request.form.to_dict(flat=False)
    args = parse_input(args)
    if len(args) == 0:
        return make_response("Must specify a criteria to delete by!",400)
    if '_id' in args:
        args['_id'] = ObjectId(args['_id'])
    # Search for and delete post
    match = {'$and': []}
    for key, value in args.items():
        match['$and'].append({key: value})
    doc = DBCLIENT['Posts'].find_one_and_delete(match)
    if doc == None:
        return make_response("Could not find post to delete!",400)
    # Delete photos associated with the post
    for filepath in doc['files']:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=filepath)
    doc['success'] = True
    return json.dumps(doc, default=str)

""" Testing API Routes """

# Returns all posts
@posts.route('/api/posts/findall', methods=['POST'])
def findall():
    cursor = DBCLIENT['Posts'].find()
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
    return json.dumps(response, indent=4, default=str)


@posts.route('/api/posts/comment', methods=['POST'])
def add_comment():
    args = request.form.to_dict(flat=False)
    args = parse_input(args)

    # check if id is valid
    if not re.match("^[0-9a-fA-F]{24}$", args['postid']):
        return make_response('Invalid post ID', 400)

    # append comment to post.comments
    result = DBCLIENT['Posts'].update(
        {'_id': ObjectId(args['postid'])}, 
        {'$push': {'comments': args['body']}})

    if not result['nModified']:
        # failed to append comment, most likely due to post not found
        return make_response('Failed to add comment, please try again', 500)
    else:
        return make_response('Added comment successfully', 200)

bkgd_upload = threading.Thread(name='upload', target=background_post_upload)
bkgd_upload.start()



# experimental profile routes

@posts.route('/api/profile/create', methods=['POST'])
def add_profile():
    args = request.form.to_dict(flat=False)
    args = parse_input(args)

    DBCLIENT['Profiles'].update(
        {'name': args['name']},
        {
            'name': args['name'],
            'fact': args['fact'],
            'picture': args['picture'],
            'stickers': []
        },
        upsert=True
    )

    # TODO: handle errors

    return make_response('Created profile successfully', 200)

@posts.route('/api/profile', methods=['POST'])
def find_profile(name=""):
    if not name:
        args = request.form.to_dict(flat=False)
        args = parse_input(args)
        name = args['name']

    result = DBCLIENT['Profiles'].find_one(
        {'name': re.compile(name, re.IGNORECASE)}
    )

    # TODO: handle errors
    if result:
        return json.dumps(result, indent=4, default=str)
    else:
        make_response("Not found", 404)

@posts.route('/api/profile/sticker', methods=['POST'])
def add_sticker():
    args = request.form.to_dict(flat=False)
    args = parse_input(args)

    print(args)

    DBCLIENT['Profiles'].update(
        {'name': args['profile']},
        {'$push': {'stickers': args}}
    )

    # TODO: handle errors

    return make_response('Added sticker successfully', 200)

'''
# script to add seniors.json data to Profiles table
directory = os.path.dirname(os.path.realpath(__file__))
with open(directory + '/static/config/seniors.json', 'r') as jsonFile:
    data = json.load(jsonFile)["seniors"]
for p in data:
    DBCLIENT['Profiles'].update(
    {'name': p['name']},
    {
        'name': p['name'],
        'fact': p['fact'],
        'picture': p['picture'],
        'stickers': []
    },
    upsert=True
)
'''