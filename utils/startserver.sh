#!/bin/bash

service mongodb start
pkill python
source ~/staffappreciation/flask/bin/activate
python ~/staffappreciation/staffappreciation/routes.py 1> ~/staffappreciation/log/log.log 2> ~/staffappreciation/log/log.log & echo "Done"


