# Dependencies
from flask import Flask

# Define the application and port
# Flask accepts a static folder parameter in which the static js and css is located
# You can refer to it using the static_url_path parameter which is the href
# used in templates, e.g. static_url_path = '/app' can be referred to as /app/main.js
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Import all views, these are all the pages or endpoints the application handles
from app import views