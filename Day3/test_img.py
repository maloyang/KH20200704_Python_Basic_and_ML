# 請填入程式
# 提示 plt.savefig('image.png')
import matplotlib.pyplot as plt
import requests
import pandas_datareader.data as web
from datetime import datetime

df = web.DataReader("2330.tw", 'yahoo', datetime(2020,1,1))
stock_date = df.index.strftime("%Y-%m-%d").tolist()
stock_close = df['Close'].tolist()

fig,ax = plt.subplots()

plt.plot(stock_date[-10:], stock_close[-10:])
plt.xlabel('date')
plt.ylabel('close')
ax.set_xticklabels(stock_date[-10:])
fig.autofmt_xdate(rotation=30)
plt.grid()

img = 'image.png'
plt.savefig(img)

token = 'xKkAS3hOquwluB4ZKfCfEAEui8HpGfwmurvm2tc8J31' #Python課程
url = "https://notify-api.line.me/api/notify"  # --> 不支援http, 只能用https
headers = {"Authorization" : "Bearer "+ token}

title = '2330近10日趨勢圖'
message =  '[%s]' %(title)
payload = {"message" :  message}
files = {'imageFile': open(img, 'rb')}
r = requests.post(url, headers = headers, params = payload, files = files)