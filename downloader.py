import urllib.request, urllib.error, json, pprint, re, time
from mysql.connector import connect, Error
import sqlite3

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
    connection = connect(
        host="localhost",
        user="root",
        password="ricky1212",
	    database="Scraper"
    )
except Error as e:
    print(e)

url_data = json.loads(my_data(url))

# iterating through the images to pull data and id
for i in url_data['data']['children']:

    print("This is the Title: {}\nThis is the Thumbnail: {}\n".format(i['data']['title'], i['data']['id']))
    
    #creating a new cursor to query the new data and eqicute the query to the database then commiting the code
    try: 
        insert = connection.cursor()
        query = "INSERT INTO images (`Title`,`Reddit_id`, `thumbnail_url`) VALUES (%s, %s, %s)"
        insert.execute(query, (i['data']['title'], i['data']['id'], i['data']['thumbnail']))
        connection.commit()
    except:
        print('skipping, image  already exists')
        continue

      #opens the url and downloads the file to a variable
    try:
            url2 = urllib.request.urlopen(i['data']['thumbnail'])
            img = url2.read()
    except ValueError as err:
            print("Download failed")
            continue

        # modifing the file name to save the image
    file_name = re.sub('[^0-9a-zA-Z]+', '-', i['data']['title'])
    file_name = "images/{}.jpg".format(file_name[0:16])

        # opening the file, truncate the file, wrighting the data in img variable, then closing
    f = open(file_name, "wb")
    f.write(img)
    f.close()

# made a new cursor to iterate through all the data form images 
new_insert = connection.cursor()
new_insert.execute("SELECT * FROM images")
rows = new_insert.fetchall()
for row in rows:
    print(row)
