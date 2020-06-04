from flask import render_template, make_response, Blueprint
from api import find_by_quarter, findall
import json

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
    
    # TODO: this does not work atm, uncomment when find_by_quarter is fixed
    # posts = json.loads(find_by_quarter(quarter)) 

    posts = json.loads(findall())
    for post in posts:
        # TODO: add logic to append corresponding post comments
        post['comments'] = ['test comment 1', 'another test comment that is also longer and will test how multiline looks']
        # TODO: below adds images to test image/gallery posts, remove before publish
        post['files'] = ['/static/postimages/testimage3.jpg', '/static/postimages/testimage2.jpg', '/static/postimages/testimage1.jpg']

    return render_template(f"feed/feed.html", title=quarter, posts=posts)

@www.route("/juniors")
def juniors():
    return render_template("juniors.html", title="juniors")

@www.route("/sharings/<name>")
def sharings(name):
    return render_template(f"sharings.html", title=f"{name} sharings", name=name)
