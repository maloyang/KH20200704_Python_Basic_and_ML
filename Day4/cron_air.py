import requests
import sqlite3
import time
import json

url = 'http://opendata.epa.gov.tw/ws/Data/AQI/?$format=json'
r = requests.get(url)
data = r.json()

# initial local DB
aqi_db = 'aqi_db.db'
conn = sqlite3.connect(aqi_db)
cursor = conn.cursor()
cursor.execute('create table IF NOT EXISTS aqi (PublishTime text NOT NULL, County text, SiteName text, AQI int, PM10 int)')
cursor.close()
conn.commit()
conn.close()

for item in data:
    if item['County'] == '高雄市':
        print('[%s %s][%s] %s, %s' %(item['County'], item['SiteName'], item['PublishTime'], item['AQI'], item['PM10']) )
        
        #- insert into local DB
        conn = sqlite3.connect(aqi_db)
        cursor = conn.cursor()
        cursor.execute("insert into aqi (PublishTime, County, SiteName, AQI, PM10) values('%s', '%s', '%s', '%s', '%s')" 
                       %(item['PublishTime'], item['County'], item['SiteName'], item['AQI'], item['PM10']))
        cursor.close()
        conn.commit()
        conn.close()