from flask import render_template, make_response, Blueprint
from api import find_by_quarter
import json
import os

www = Blueprint('www', __name__)

"""
Routes for GET requests
"""
@www.route("/")
@www.route("/index")
def index():
    return render_template("index.html", title="landing")

@www.route("/feed/<quarter>")
def feed(quarter):
    if quarter not in ['fall', 'winter', 'spring']:
        return make_response("Quarter must be 'fall', 'winter' or 'spring'", 404)
    
    memory = {'title': 'A title/short caption here', 'body': f'Summarize {quarter} quarter here, perhaps highlight some memories'}

    posts = json.loads(find_by_quarter(quarter))

    # process the posts, append additional info if needed
    for post in posts:
        # TODO: add logic to append corresponding post comments
        # post['comments'] = ['test comment 1', 'another test comment that is also longer and will test how multiline looks']
        if not post['author']: post['author'] = "Anonymous"

    return render_template(f"feed/feed.html", title=quarter, memory=memory, posts=posts)

@www.route("/juniors")
def juniors():
    directory = os.path.dirname(os.path.realpath(__file__))
    with open(directory + '/static/config/juniors.json', 'r') as f:
        cfg = json.load(f)
    return render_template("juniors/juniors.html", title="juniors", juniors=cfg['juniors'])

@www.route("/sharings/<name>")
def sharings(name):
    return render_template(f"sharings.html", title=f"{name} sharings", name=name)
