import requests 
import base64 
import json

URL = "http://localhost:5000/"
imageExtension = '.jpg'
# Image

#http://localhost:5000/image/all [GET]
def recoverImages():
    resource = URL + 'image/all'
    r = requests.get(url = resource)
    imageList = r.json()
    print(imageList)

#http://localhost:5000/image/<id> [GET]
def recoverEspecificImage(id):
    resource = URL + 'image/' + id
    r = requests.get(url = resource)
    imageJson = r.json()
    
    image_64_encode = imageJson['image_data']
    image_64_encode = image_64_encode.encode("utf-8")
    image_64_decode = base64.decodebytes(image_64_encode) 

    fileName = imageJson['ID'] + imageExtension

    with open(fileName, 'wb') as image_result:
        image_result.write(image_64_decode)

#http://localhost:5000/info [GET]
def recoverStorageInfo():
    resource = URL + 'info'
    r = requests.get(url = resource)
    info = r.json()
    print(info)

#http://localhost:5000/image [POST]
def insertImage(id):
    resource = URL + 'image'
    json_file = {}
    json_file['ID'] = id

    image = open( id + imageExtension, 'rb') 
    image_read = image.read() 
    image_64_encode = base64.encodestring(image_read) 
    image_64_encode = image_64_encode.decode("utf-8")

    json_file['image_data'] = image_64_encode

    r = requests.post(url = resource , json = json_file)
    print(r)

#http://localhost:5000/image/example.jpg [DELETE]
def removeOneImage(id):
    resource = URL + 'image/' + id
    r = requests.delete(url = resource)
    print(r)

#http://localhost:5000/image/all [DELETE]
def removeAllImages():
    resource = URL + 'image/all'
    r = requests.delete(url = resource)
    print(r)



# --------//--------- Examples --------//---------

#Description
#insertImage("example")

#Description
#recoverImages()

#Description
#recoverEspecificImage("example")

#Description
#recoverStorageInfo()

#Description
#removeOneImage("example")

#Description
#removeAllImages()

