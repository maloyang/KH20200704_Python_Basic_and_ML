# -*- coding: utf-8 -*-

import os
import random
import time
import requests

from flask import Flask, request, abort, render_template, send_file
from flask import json, jsonify
from flask_cors import CORS, cross_origin # for cross domain problem

import sqlite3
import time
import json
from sqlalchemy import create_engine

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


#app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# add "+pymysql" in url
url = os.getenv('JAWSDB_URL', None) # 直接由heroku環境變數取得DB的url
#因為格式中沒有指定使用pymysql會有問題，所以自己加入這個字眼
mysql_db_url = 'mysql+pymysql' + url[5:]
my_db = create_engine(mysql_db_url)

aqi_db = 'aqi_db.db'

@app.route('/')
def airbox():
    return app.send_static_file('index.html')

@app.route('/api/data/last', methods=['GET'])
def api_data_last():
    SiteName = request.args.get('SiteName') #ex: 左營
    if not SiteName:
        SiteName = '左營'
    # 開始下SQL資料取資料
    #SiteName = '左營'
    conn = sqlite3.connect(aqi_db)
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM aqi WHERE SiteName = '%s' ORDER BY PublishTime DESC limit 1" %(SiteName) )
    rows = res.fetchall()

    data_list = list(rows)

    return jsonify(data_list[0])

@app.route('/api/data/history', methods=['GET'])
def api_data_history_get():
    SiteName = request.args.get('SiteName') #ex: 左營
    if not SiteName:
        SiteName = '左營'

    # 取出最近的資料
    conn = sqlite3.connect(aqi_db)
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM aqi WHERE SiteName = '%s' ORDER BY PublishTime DESC limit 12" %(SiteName) )
    rows = res.fetchall()

    data_list = list(rows)

    def take_time(elem):
        return elem[0]
    data_list.sort(key=take_time)

    return jsonify(data_list)

@app.route('/api/mysql/data/last', methods=['GET'])
def api_mysql_data_last():
    SiteName = request.args.get('SiteName') #ex: 左營
    if not SiteName:
        SiteName = '左營'
    # 開始下SQL資料取資料
    #SiteName = '左營'
    resultProxy=my_db.execute("select * from my_aqi  WHERE SiteName = '%s' ORDER BY PublishTime DESC limit 1" %(SiteName))
    data = resultProxy.fetchall()
    print('data:', data)

    return jsonify(list(data[0]))


@app.route('/api/mysql/data/history', methods=['GET'])
def api_mysql_data_history_get():
    SiteName = request.args.get('SiteName') #ex: 左營
    if not SiteName:
        SiteName = '左營'

    resultProxy=my_db.execute("select * from my_aqi  WHERE SiteName = '%s' ORDER BY PublishTime DESC limit 12" %(SiteName))
    data = resultProxy.fetchall()
    print('data:', data)

    data_list = []
    for item in data:
        data_list.append(list(item))

    return jsonify(data_list[-1::-1])

@app.route('/api/mysql/data/chart', methods=['GET'])
def api_mysql_data_chart_get():
    SiteName = request.args.get('SiteName') #ex: 左營
    if not SiteName:
        SiteName = '左營'

    resultProxy=my_db.execute("select * from my_aqi  WHERE SiteName = '%s' ORDER BY PublishTime DESC limit 12" %(SiteName))
    data = resultProxy.fetchall()
    print('data:', data)
    data_list = []
    for item in data:
        data_list.append(list(item))

    tsp_list = []
    time_list = []
    for item in data_list[-1::-1]:
        time_list.append(item[0])
        tsp_list.append(item[3])
    font = FontProperties(fname=r"NotoSansTC-Regular.otf", size=14)
    fig,ax = plt.subplots(figsize=(12,8))
    plt.plot(time_list, tsp_list, '-o')

    plt.xlabel('月份', fontproperties = font)
    plt.ylabel('總懸浮微粒μg/m^3', fontproperties = font)
    #plt.xticks(time_list, rotation=60)
    ax.set_xticklabels(time_list)
    fig.autofmt_xdate(rotation=30)
    plt.grid()
    fn_chart = 'chart.png'
    plt.savefig(fn_chart)

    return send_file(fn_chart, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, port=80)
