import base64
import csv
import json
import logging
import os
import os.path

# import preview as pre
import random
import wave
from base64 import b64encode
from cgi import print_arguments
from io import StringIO
from mimetypes import guess_extension
from os import path

import flask
import numpy as np
import requests

# from flask_session import Session
from engineio.payload import Payload
from flask import (
    Flask,
    abort,
    current_app,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

Payload.max_decode_packets = 50

app = Flask(__name__, static_url_path='/static') 
            
app.debug = False
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_TYPE"] = "filesystem"

#socketio = SocketIO(app, manage_session=False)
#app, extensions = load_extensions.load(app)

### HTML ROUTES ###


### Execute code before first request ###
@app.before_first_request
def execute_before_first_request():
    print("startup")


@app.route("/main")
def index():
    return flask.redirect("/main")



