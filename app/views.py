# Include our application
from app import app
from flask import render_template, request, redirect, url_for
from os import path
from werkzeug.utils import secure_filename
import json

# Define a route which will capture all routes and link them back to index
@app.route('/', defaults = {'path': ''})
@app.route('/<path:path>')
def index(path):

    # Return the index page. By default, Flask will look into a /templates folder
    return render_template('index.html')

# Define upload behavior
UPLOAD_FOLDER = path.join('model', 'input')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a route which the client can post images to, note that after each meshroom process
# these images will be deleted
@app.route('/upload', methods=['POST'])
def upload():

    # Check if the post request has the file part
    if 'input' not in request.files:
        raise Exception("Missing parameter: input")

    # Iterate over all the files
    for file in request.files.getlist('input'):

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            raise Exception("file could not be uploaded")

        if file and 'image' in file.mimetype:
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            raise Exception("file could not be uploaded")

    # Everything has been uploaded
    return {}

# Define a route which the client can post json to. This JSON will override the default configuration
# of the meshroom process. This JSON override should be removed after the meshroom process finishes
# The client can also request the default config
@app.route('/config', methods=['GET', 'POST'])
def config():

    # Handle GET request
    if request.method == 'GET':

        # Fetch the default configuration
        with open(path.join('model', 'default.json'), 'r') as f:

            # And expose its contents to the client
            return f.read()
    
    # Handle POST request
    if request.method == 'POST':

        # Check if the post request has json data
        if 'config' not in request.form:
            raise Exception("Missing parameter: config")

        # Check if the JSON is valid
        try:
            data = json.loads(request.form['config'])
        except Exception:
            raise Exception("JSON data is invalid")

        # At this point, we have valid JSON data, which we can store in a temporary file
        with open(path.join('model', 'tmp_config.json'), 'w') as f:

            # Write the JSON data to the temporary file
            f.write(json.dumps(data))

        # Everything is complete
        return {}