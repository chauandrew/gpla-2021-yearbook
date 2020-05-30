# Staff Appreciation Website

## Directory Structure

```bash
root 
 |--api  # Back End Service
 |   |--api.py         # Backend rest framework using Flask
 |   |--startserver.sh # Restarts server in subprocess on ubuntu
 |   |--stopserver.sh  # Stops server in subprocess on ubuntu
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
It all runs in Flask, so:
1. Create a virtualenv
```bash
pip3 install virtualenv
virtualenv flask
source flask/bin/activate
```
2. `pip install -r requirements.txt`

## Starting the server:
1. Start your virtualenv
2. `python api/api.py

## Rest API Documentation:
Every request here is a post request. 

### Insert: insert a post into the backend
- url: `http://ec2-184-169-199-121.us-west-1.compute.amazonaws.com:5000/insert`
Arguments:
- date (required), formatted `YYYY-MM-DD`
- quarter (required), `FALL`, `WINTER`, or `SPRING`
- type (required), `ALBUM`, `PHOTO`, or `MEMORY`
- path (required), the local path to an image, description, or album. For images (`*.png` or `*.jpg*`) and descriptions (`*.txt`), use the direct path to the image. For albums, take the path to a folder containing all it's contents. 
- title (optional), a title for the post
- description (optional), a description for the post


### Write a comment: 
- url: `http://ec2-184-169-199-121.us-west-1.compute.amazonaws.com:5000/posts/<quarter>/comment`
Arguments:
- quarter (required), `fall`, `winter`, or `spring`. 
- author (required), a comment's author
- body (required), the content of a comment
- path (required), the local path to a post, must match the path used in `insert`.


### Find By Quarter: find paginated posts by quarter
- url: `http://ec2-184-169-199-121.us-west-1.compute.amazonaws.com:5000/posts/<quarter>`
Arguments:
- quarter (required), `fall`, `winter`, or `spring`. 
- page (required), argument for pagination. Using page=0 will return the first 3 posts, page=1 will give the next 3, and so on. These are sorted by date. 


### Delete: delete matching posts
- url: `http://ec2-184-169-199-121.us-west-1.compute.amazonaws.com:5000/remove`
This deletes by equality based on the parameters you pass in. There are no required arguments, but you must use at least one filtering criteria. If you pass the parameters `'date': 2020-05-29`, this will delete one post that matches that criteria.


### Find All: Get all posts in database
- url: `http://ec2-184-169-199-121.us-west-1.compute.amazonaws.com:5000/posts/findall`


  