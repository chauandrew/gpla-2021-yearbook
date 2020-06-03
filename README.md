# Staff Appreciation Website

## Directory Structure

```bash
root 
 |--staffappreciation  # Webapp
     |--app.py     # flask app template
     |--www.py     # get request routes
     |--api.py     # backend post request routes
     |--config.py  # python settings and configs
     |--static     # css, images, js
     |--templates  # html files
 |--bootstrap-4.5.0-examples # Bootstrap examples to copypaste from
     |...
 | 
 |--requirements.txt  # requirements to pip install from
 |--README.md         # this file
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
2. `python staffappreciation/app.py
3. Navigate to `http://localhost:5000/`

## Rest API Documentation:
Every request here is a post request. 

### Upload: insert a post into the backend
- url: `/upload`
Arguments:
- date (required), formatted `YYYY-MM-DD`
- quarter (required), `FALL`, `WINTER`, or `SPRING`
- path (required), the local path to an image, description, or album. For images (`*.png` or `*.jpg*`) and descriptions (`*.txt`), use the direct path to the image. For albums, take the path to a folder containing all it's contents. 
- title (optional), a title for the post
- body (optional), a description for the post


### Write a comment: 
- url: `/posts/comment`
Arguments:
- author (required), a comment's author
- body (required), the content of a comment
- _id (required), the object id of a post


### Find By Quarter: find paginated posts by quarter
- url: `/posts/<quarter>`
Arguments:
- quarter (required), `fall`, `winter`, or `spring`. 
- page (required), argument for pagination. Using page=0 will return the first 3 posts, page=1 will give the next 3, and so on. These are sorted by date. 


### Delete: delete matching posts
- url: `/remove`
This deletes by equality based on the parameters you pass in. There are no required arguments, but you must use at least one filtering criteria. If you pass the parameters `'date': 2020-05-29`, this will delete one post that matches that criteria.


### Find All: Get all posts in database
- url: `/posts/findall`


  