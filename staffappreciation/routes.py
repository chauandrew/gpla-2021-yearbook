from flask import Flask, request, jsonify, render_template, make_response
from flask_pymongo import PyMongo
import pymongo

import re
import datetime
import json
from bson import ObjectId

PAGE_SIZE=3

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["FlaskApp"]
posts = mydb["Posts"]

# JSONEncoder from stack overflow :)
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JsonEncoder.default(self, o)

# Turn single length arrays into standalone objects
def parse_input(args):
    for k, v in args.items():
        if isinstance(v, list) and len(v) == 1:
            args[k] = v[0]
    return args

"""
Routes for GET requests
"""

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="landing")

@app.route("/feed/<quarter>")
def feed(quarter):
    print(quarter)
    if quarter not in ['fall', 'winter', 'spring']:
        return("404")
    return render_template(f"feed.html", title=quarter)

@app.route("/juniors")
def juniors():
    return render_template("juniors.html", title="juniors")

@app.route("/sharings/<name>")
def sharings(name):
    return render_template(f"sharings.html", title=f"{name} sharings", name=name)

"""
Routes for API/POST requests related to the database.
"""

# Insert a post into the database
@app.route("/insert", methods=['POST'])
def insert():
    args = request.form.to_dict(flat=False)
    args = parse_input(args)
    # Type Checking
    if 'date' not in args:
        return "'date' field is required"
    elif not re.match("^\d\d\d\d/\d\d/\d\d$", str(args['date'])):
        return "date must look like: 'YYYY/MM/DD'"
    if 'quarter' not in args:
        return "'quarter' field is required. must be 'FALL', 'WINTER', or 'SPRING'"
    elif args['quarter'] not in ['FALL', 'WINTER', 'SPRING']:
        return "'quarter' field must be 'FALL', 'WINTER', or 'SPRING'"
    if 'type' not in args:
        return "'type' field is required. Must be 'ALBUM', 'PHOTO', or 'MEMORY'"
    elif args['type'] not in ['ALBUM', 'PHOTO', 'MEMORY']:
        return "'type' field must be 'ALBUM', 'PHOTO', or 'MEMORY'"
    if 'path' not in args:
        return "'path' field is required. It describes the path to appropriate data"
    # Match by all specified fields
    match = {'$and': []}
    for key, value in args.items():
        match['$and'].append({key: value})
    result = posts.update_one(match, {'$set':args}, upsert=True)
    response = {'acknowledged': result.acknowledged, 
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
            'raw_result': result.raw_result,
            'upserted_id': result.upserted_id }
    return JSONEncoder().encode(response)

# Returns all posts
@app.route('/posts/findall', methods=['POST'])
def findall():
    cursor = posts.find()
    response = [doc for doc in cursor]
    return JSONEncoder().encode(response)

# Finds posts in a given quarter, sorted / paginated by date
@app.route('/posts/<quarter>', methods=['POST'])
def find_by_quarter(quarter):
    if quarter.lower() not in ['fall', 'winter', 'spring']:
        return "quarter (path) must be 'fall', 'winter', or 'spring'"
    args = request.form.to_dict(flat=False)
    # turn single length arrays into standalone objects, etc.
    args = parse_input(args)
    pagenum = int(args['page'])
    front = pagenum * PAGE_SIZE
    back = front + PAGE_SIZE
    cursor = posts.find({'quarter': quarter.upper()})
    cursor.sort('date', pymongo.ASCENDING)

    #response = cursor
    response = [doc for doc in cursor[front:back]]
    return JSONEncoder().encode(response)

# Removes a post
@app.route("/remove", methods=['POST'])
def remove():
    args = request.form.to_dict(flat=False)
    args = parse_input(args)
    if len(args) == 0:
        return "Must specify a criteria to delete by!"
    match = {'$and': []}
    for key, value in args.items():
        match['$and'].append({key: value})
    result = posts.delete_one(match) 
    response = {'acknowledged': result.acknowledged, 
            'deleted_count': result.deleted_count,
            'raw_result': result.raw_result}
    return JSONEncoder().encode(response)

# Write a comment
@app.route('/posts/<quarter>/comment', methods=['POST'])
def write_comment(quarter):
    if quarter.lower() not in ['fall', 'winter', 'spring']:
        return "quarter (path) must be 'fall', 'winter', or 'spring'"
    args = request.form.to_dict(flat=False)
    args = parse_input(args)
    # Validate arguments
    if 'author' not in args:
        return "Must specify 'author' of comment"
    if 'body' not in args:
        return "Must specify 'body' of comment"
    if 'path' not in args:
        return "Must specify 'path' of post that comment links to"
    # Search for post
    match = {'$and': [{'quarter':quarter.upper()}, {'path':args['path']}]}
    if posts.count_documents(match) <= 0:
        return f"Could not find post with path {args['path']}"
    cursor = posts.find(match)
    # Add comment to post
    comments = []
    if 'comments' in cursor[0]:
        comments = cursor[0]['comments']
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comments.append({'body': args['body'], 
                     'author': args['author'],
                     'timestamp': now})
    result = posts.update_one(match, {'$set':{'comments':comments}})
    response = {'acknowledged': result.acknowledged, 
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
            'raw_result': result.raw_result,
            'upserted_id': result.upserted_id }
    return JSONEncoder().encode(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
