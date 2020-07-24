# -*- coding: utf-8 -*-
#===========================================
# 版本說明
#-------------------------------------------
#===========================================

import os
import random
import requests
import datetime, time
import csv

from functools import wraps
from flask import Flask, request, abort, render_template, Response
from flask import json, jsonify, session, redirect, url_for
from flask import send_file

VER = 'V2020.07.17'

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/test')
def test():
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return jsonify({'result':'OK', 'localtime':local_time, 'version':VER})

@app.route('/day2-1')
def day2_1():
    return app.send_static_file('day2-1.html')

@app.route('/')
def index():
    return 'OK'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
