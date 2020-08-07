from flask import Flask
from flask_cors import CORS
app = Flask(__name__) # makes app a member of the parent dir module
CORS(app)

from flask_app import routes # workaround for circular dependencies


