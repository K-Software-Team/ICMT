import requests, json

userjson = open("config/user.json").read()
username = json.loads(userjson)['user'][0]
userpwd = json.loads(userjson)['user'][1]
site = json.loads(open("config/global.json").read())['site']

print(requests.post(site + "/api/signup.php", data={"username": username, "password": userpwd}).text)