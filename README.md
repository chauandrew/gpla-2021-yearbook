# Staff Appreciation Website

## Directory Structure

```bash
root 
 |--api  # Back End Service
 |
 |--www  # Front End Service
 |   |--css       # Style sheets
 |   |--images    # Image Files
 |   |--js        # site-wide javascript
 |   -*.html      # various static html files (to be organized better)
 |
 |--bootstrap-4.5.0-examples # Bootstrap examples to copypaste from
 | 
 -requirements.txt  # requirements to pip install from
 -README.md         # this file
```

## Setting up backend:
It all runs in Django, so:
1. Create a virtualenv
```bash
pip3 install virtualenv
virtualenv myenvname
source myenvname/bin/activate
```
2. `pip install -r requirements.txt`

## Starting the server:
1. Start your virtualenv
2. `python api/manage.py runserver

