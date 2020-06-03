from flask import Flask
from api import Blueprint

import config
from api import api
from www import www

app = Flask(__name__)
app.register_blueprint(www)
app.register_blueprint(api)

# Locally import routes

""" Main """
if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.run()
