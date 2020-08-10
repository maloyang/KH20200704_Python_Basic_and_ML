import requests
import sqlite3
import time
import json
import os

from sqlalchemy import create_engine
# add "+pymysql" in url
url = os.getenv('JAWSDB_URL', None) # 直接由heroku環境變數取得DB的url
#因為格式中沒有指定使用pymysql會有問題，所以自己加入這個字眼
mysql_db_url = 'mysql+pymysql' + url[5:]
my_db = create_engine(mysql_db_url)

# check and create table
print('check table exist?')
str_cmd = 'create table IF NOT EXISTS my_aqi (PublishTime text NOT NULL, County text, SiteName text, AQI int, PM10 int)'
resultProxy = my_db.execute(str_cmd)

# data source
print('get air data')
url = 'http://opendata.epa.gov.tw/ws/Data/AQI/?$format=json'
r = requests.get(url)
data = r.json()
print('len(data): ', len(data))

for item in data:
    if item['County'] == '高雄市':
        print('[%s %s][%s] %s, %s' %(item['County'], item['SiteName'], item['PublishTime'], item['AQI'], item['PM10']) )

        #- insert into mysql db
        str_cmd = ("insert into my_aqi (PublishTime, County, SiteName, AQI, PM10) values('%s', '%s', '%s', '%s', '%s')" 
                    %(item['PublishTime'], item['County'], item['SiteName'], item['AQI'], item['PM10']) )
        resultProxy=my_db.execute(str_cmd)
                 
