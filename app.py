from flask import Flask
# from posts import Blueprint

import config
from posts import posts
from www import www
from timeline import timeline

app = Flask(__name__)
app.register_blueprint(www)
app.register_blueprint(posts)
app.register_blueprint(timeline)

# Locally import routes

""" Main """
if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.jinja_env.cache = {}
    app.run()
