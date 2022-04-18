import urllib.request, json, pprint

url = "https://www.reddit.com/r/funnypictures.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

for i in data['data']['children']:
    print("This is Title: {}\nThis is Thimbnail: {}\n".format(i['data']['title'], i['data']['thumbnail']))


##data = json.loads(url)




