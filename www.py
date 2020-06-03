from flask import render_template, make_response, Blueprint

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
    return render_template(f"feed/feed.html", title=quarter)

@www.route("/juniors")
def juniors():
    return render_template("juniors.html", title="juniors")

@www.route("/sharings/<name>")
def sharings(name):
    return render_template(f"sharings.html", title=f"{name} sharings", name=name)
