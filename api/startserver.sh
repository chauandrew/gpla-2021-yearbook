#!/bin/bash

service mongodb start
pkill python
source ~/staffappreciation/flask/bin/activate
python ~/staffappreciation/api/api.py 1> ~/staffappreciation/api/log.log 2> ~/staffappreciation/api/log.log & echo "Done"


