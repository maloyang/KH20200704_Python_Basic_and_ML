# 第一個line雲端排程用程式 --> 用vscode或是notepad++存成 `test.py`

import requests

token = 'bT0rhcsiaSaiK8ulEKj7Gi4ZtS1ht9Q9WKUoVtfvGFc'
#token = 'xKkAS3hOquwluB4ZKfCfEAEui8HpGfwmurvm2tc8J31' #Python課程

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ token}

title = 'Malo雲端伺服器'
message =  '[%s] 雲端排程發送訊息' %(title)
payload = {"message" :  message}

r = requests.post(url ,headers = headers ,params=payload)