import requests
url = 'https://m.manhua39.com/manhua/bennvhai/1263214-2.html'

print(requests.get(url).content)
