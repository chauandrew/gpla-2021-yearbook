from flask import render_template, make_response, Blueprint
from posts import find_by_quarter, findall, find_profile
from timeline import get_events
from config import DEBUG
import json
import os

www = Blueprint('www', __name__)

"""
Routes for GET requests
"""
@www.route("/")
@www.route("/index")
def index():
    return render_template("index.html", title="GPLA 2021 Yearbook")

@www.route("/timeline")
def timeline():
    directory = os.path.dirname(os.path.realpath(__file__))
    events = json.loads(get_events()) # A list of events
    events.sort(key=lambda e: e['date'])
    return render_template(f"timeline/timeline.html", title=f"Timeline", events=events)

@www.route("/seniors")
def seniors():
    directory = os.path.dirname(os.path.realpath(__file__))
    with open(directory + '/static/config/seniors.json', 'r') as jsonFile:
        cfg = json.load(jsonFile)
    return render_template("wip.html", title="Coming Soon") # remove once we finish the page
    return render_template("seniors/seniors.html", title="Seniors", seniors=cfg['seniors'])

@www.route("/memories")
def memories():
    directory = os.path.dirname(os.path.realpath(__file__))

    posts = json.loads(findall())

    # process the posts, append additional info if needed
    for post in posts:
        if not post['author']: post['author'] = "Anonymous"
        # strip aws link for testimages
        if DEBUG:
            photo_paths = []
            for photo in post['files']:
                if "testimage" in photo:
                    photo_paths.append(photo.replace("https://staff-appreciation.s3.amazonaws.com/", "").split('?')[0])
                else:
                    photo_paths.append(photo)
            post['files'] = photo_paths

    return render_template(f"feed/feed.html", title=f"Memories", posts=posts)

@www.route("/profile/<name>")
def profile(name):

    profile = json.loads(find_profile(name))
    
    if not profile or profile == "null":
        return make_response("Could not find person", 404)

    print(profile)
    profile['picture'] = f"/{profile['picture']}"

    return render_template("profile/profile.html", title=profile["name"], profile=profile)