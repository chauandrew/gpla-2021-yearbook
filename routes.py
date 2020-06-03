from __main__ import app
# import config

from flask import Flask, request, jsonify, render_template, make_response


"""
Routes for GET requests
"""
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="landing")

@app.route("/feed/<quarter>")
def feed(quarter):
    if quarter not in ['fall', 'winter', 'spring']:
        return make_response("Quarter must be 'fall', 'winter' or 'spring'", 404)
    return render_template(f"feed/feed.html", title=quarter)

@app.route("/juniors")
def juniors():
    return render_template("juniors.html", title="juniors")

@app.route("/sharings/<name>")
def sharings(name):
    return render_template(f"sharings.html", title=f"{name} sharings", name=name)
