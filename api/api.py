from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["FlaskApp"]
posts = mydb["Posts"]

@app.route("/insert", methods=['POST'])
def insert():
    # TODO: type checking, turn single length arrays into standalone objects, etc.
    args = request.args.to_dict(flat=False)
    print(args)
    match = {'id': args['id']}
    x = posts.update(match, args, upsert=True)
    return request.args

@app.route("/remove", methods=['POST'])
def remove():
    args = request.args.to_dict(flat=False)
    match = {}
    for key, value in args.items():
        match[key] = value
    ok = posts.delete_one(match)
    print(match, ok)
    return request.args
            

if __name__ == "__main__":
    app.run(host='0.0.0.0')
