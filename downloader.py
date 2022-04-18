import urllib.request, json, pprint, re

url = "https://www.reddit.com/r/adoptme.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

for i in data['data']['children']:
    print("This is Title: {}\nThis is Thimbnail: {}\n".format(i['data']['title'], i['data']['thumbnail']))
    
    try:
        url2 = urllib.request.urlopen(i['data']['thumbnail'])
        img = url2.read()
    except ValueError as err:
        print("Download failed")
        continue

    file_name = re.sub('[^0-9a-zA-Z]+', '-', i['data']['title'])
    file_name = "images/{}.jpg".format(file_name[0:16])
    f = open(file_name, "wb")
    f.write(img)


   


##data = json.loads(url)




