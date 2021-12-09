from flask import Flask
from flask_cors import CORS
app = Flask(__name__) # makes app a member of the parent dir module
CORS(app)

from b_note_backend import routes # workaround for circular dependencies


