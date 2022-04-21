import urllib.request, urllib.error, json, pprint, re, time
from mysql.connector import connect, Error

print("Starting Scraper")

url = "https://www.reddit.com/r/funnypictures.json"


def  my_data(url):
    
    print("downloading {}".format(url))

    try:
        url_response = urllib.request.urlopen(url)
        return url_response.read()
    except:
        print("There was an error, trying again")

    time.sleep(5)
    return my_data(url)


try:
    connection =  connect(
        host="localhost",
        user="root",
        password="ricky1212",
	    database="Scraper"
    )
except Error as e:
    print(e)

url_data = json.loads(my_data(url))


for i in url_data['data']['children']:

    print("This is the Title: {}\nThis is the Thimbnail: {}\n".format(i['data']['title'], i['data']['thumbnail']))
    
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
    f.close()

    insert = connection.cursor()
    query = "INSERT INTO images (`Title`,`Reddit_id`) VALUES (%s, %s)"
    insert.execute(query, (i['data']['title'], i['data']['thumbnail']))
    connection.commit()

   


##data = json.loads(url)




