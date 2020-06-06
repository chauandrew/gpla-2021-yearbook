# Staff Appreciation Website

## Directory Structure

```python
/staffappreciation # root
  /staticd
    /config     # files to store text, etc. rather than directly in html
    /css        # stylesheets
    /images     # static images, organized further
       ...
    /js         # js for front-end animations
  /templates    # html files
    /common     # header, footer, metadata, scripts
    /feed       # Templates for the fall/winter/spring pages
    /post
    /juniors    
  
app.py     # flask app template
www.py     # get requests
api.py     # backend post requests routes
config.py  # python settings, global variables, configurations
 
requirements.txt  # requirements to pip install from
README.md         # this file
```

## Setting up the backend:
The project is built using Flask and Jinja2! Here's a intro of how to get started:
1. Create a virtualenv
```bash
pip3 install virtualenv     # Install virtualenv
virtualenv flask            # Create a virtualenv named flask
source flask/bin/activate   # Start the virtual environment
```
2. `pip install -r requirements.txt` to install all the necessary packages

## Starting the server:
1. Start your virtualenv
2. From the root directory, run: `FLASK_APP=app.py FLASK_ENV=development flask run`
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
- url: `/comment`
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


  