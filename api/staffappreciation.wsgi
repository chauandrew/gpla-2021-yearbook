#!/usr/bin/env python

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/mnt/c/A2F/staffappreciation/api')
from my_flask_app import app as application
application.secret_key = 'secretsecretsecret'
