# -*- coding: utf-8 -*-

import os
import random
import time
import requests

from flask import Flask, request, abort, render_template
from flask import json, jsonify

#app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/')
def airbox():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(debug=True)
