
import requests

token = 'bT0rhcsiaSaiK8ulEKj7Gi4ZtS1ht9Q9WKUoVtfvGFc'
#token = 'xKkAS3hOquwluB4ZKfCfEAEui8HpGfwmurvm2tc8J31' #Python課程

url = "https://notify-api.line.me/api/notify"  # --> 不支援http, 只能用https
headers = {"Authorization" : "Bearer "+ token}

title = 'Malo御用'
message =  '[%s] 課程demo' %(title)
payload = {"message" :  message}

r = requests.post(url ,headers = headers ,params=payload)
r