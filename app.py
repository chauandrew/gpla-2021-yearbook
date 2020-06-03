from flask import Flask

app = Flask(__name__)

# Locally import routes
import routes
import api
import config

""" Main """
if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.run()
