from config import DBCLIENT
from config import UPLOAD_FOLDER
from config import COMPRESSION_KEY

from flask import request, jsonify, render_template, make_response, Blueprint
import pymongo
from werkzeug.utils import secure_filename
import tinify # for compression api

import os
from pathlib import Path
import re
import datetime
import json
from bson import ObjectId

api = Blueprint('api', __name__)

PAGE_SIZE=3
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.jpeg']
tinify.key = COMPRESSION_KEY

# Turn single length arrays into standalone objects
def parse_input(args):
    for k, v in args.items():
        if isinstance(v, list) and len(v) == 1:
            args[k] = v[0]
    return args

# Upload a post! needs: 'date', 'quarter', and ('files' or 'author','body')
@api.route("/upload", methods=['POST'])
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
    if 'quarter' not in args:
        return "'quarter' field is required. must be 'FALL', 'WINTER', or 'SPRING'"
    elif args['quarter'] not in ['FALL', 'WINTER', 'SPRING']:
        return make_response("'quarter' field must be 'FALL', 'WINTER', or 'SPRING'",400)
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

    # upload each file to filesystem
    paths = []
    now = str(datetime.datetime.now()).replace(' ','')
    upload_folder = f"{UPLOAD_FOLDER}/{now}"
    dirname = os.path.dirname(os.path.realpath(__file__)) # use absolute paths when saving files, local paths in directory
    Path(dirname + upload_folder).mkdir(parents=True, exist_ok=True)
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join(upload_folder, filename)
        file.save(dirname + path)
        paths.append(path)
    args['files'] = paths
    args['comments'] = []
    # Upload to database and return
    result = DBCLIENT['Posts'].insert_one(args)
    if not result.acknowledged: # if upload fails, delete files and return error
        for path in paths:
            os.remove(dirname + path)
        os.rmdir(os.path.dirname(paths[0]))
        return "Failed to save post to database!"
    else: 
        compress_images(paths)
        args.update({'acknowledged': result.acknowledged, 'document_id': result.inserted_id })
        return json.dumps(args, default=str)

# Finds posts in a given quarter, sorted / paginated by date
@api.route('/posts/<quarter>', methods=['POST'])
def find_by_quarter(quarter):
    if quarter.lower() not in ['fall', 'winter', 'spring']:
        return make_response("quarter (path) must be 'fall', 'winter', or 'spring'", 400)
    args = request.form.to_dict(flat=False)
    # turn single length arrays into standalone objects, etc.
    args = parse_input(args)
    cursor = DBCLIENT['Posts'].find({'quarter': quarter.upper()})
    cursor.sort('date', pymongo.ASCENDING)
    if 'page' in args:
        front = int(args['page']) * PAGE_SIZE
        response = [doc for doc in cursor[front:front + back]]
        return json.dumps(response, default=str)
    else:
        response = [doc for doc in cursor]
        return json.dumps(response, default=str)


# Removes a post using any available criteria to match
@api.route("/remove", methods=['POST'])
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
        os.remove(filepath)
    os.rmdir(os.path.dirname(doc['files'][0]))
    doc['success'] = True
    return json.dumps(doc, default=str)

# Write a comment. Find post by ObjectId
@api.route('/posts/comment', methods=['POST'])
def write_comment():
    # Parse arguments
    args = request.form.to_dict(flat=False)
    args = parse_input(args)
    if 'author' not in args:
        return make_response("Must specify 'author' of comment",400)
    if 'body' not in args:
        return make_response("Must specify 'body' of comment",400)
    if '_id' not in args:
        return make_response("Must specify '_id' of post comment attaches to",400)
    # Search for post
    match = {'_id': ObjectId(args['_id'])}
    if DBCLIENT['Posts'].count_documents(match) <= 0:
        return make_response(f"Could not find post with path {args['path']}",400)
    doc = DBCLIENT['Posts'].find_one(match)
    if 'comments' not in doc:
        doc['comments'] = []
    # Add comment to post
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc['comments'].append({'body': args['body'], 
                     'author': args['author'],
                     'timestamp': now})
    result = DBCLIENT['Posts'].update_one(match, {'$set':{'comments':doc['comments']}})
    doc.update({'acknowledged': result.acknowledged, 
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
            'raw_result': result.raw_result,
            'upserted_id': result.upserted_id })
    return json.dumps(doc, default=str)


""" Testing API Routes """

# Returns all posts
@api.route('/posts/findall', methods=['POST'])
def findall():
    cursor = DBCLIENT['Posts'].find()
    response = [doc for doc in cursor]
    return json.dumps(response, indent=4, default=str)

def compress_images(filepaths):
    if COMPRESSION_KEY == "": # don't compress locally
        return
    for path in filepaths:
        source = tinify.from_file(path) # compress
        source.to_file(path)            # upload compressed
