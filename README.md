# Image Storage 

Now you can storage image in remote machine using HTTP requests.

![](readme/ImageStorage-en.png)

Icons made by Those Icons and catkuro from 'www.flaticon.com'

## 1. Usage

You need an environment with Python 3.x and packages listed on requirements.txt file. 

1. Install packages listed on requirements file.
```shell
pip3 install -r requirements.txt
```

2. Clone this project. 
```shell
git clone https://github.com/ebsouza/ImageStorage.git
```

3. Enter into project folder.
```shell
cd ImageStorage
```

4. Run the API.
```shell
$ python run.py
```

5. Check the returned message. 
```shell
# The server will send this string -> 'Image Storage API. by: Erick Barbosa'
$ curl http://localhost:5000/
```


## 2. Test

Run all tests with test.py script.

```shell
$ python test.py
```

## 3. API Resources

**image**

[POST]

> http://localhost:5000/image
>
> Send a json = {'ID': image_id , 'image_data': image_base64} to API


[GET]

> http://localhost:5000/image/<image_id>
>
> Return the image 'image_id.extension'


[GET]

> http://localhost:5000/image
>
> Return a json list [{'file_name' : file name with extension , 'size (Mb)' : image size in Mb}]


[DELETE]

> http://localhost:5000/image/<image_id>
>
> Remove a specific image


> http://localhost:5000/image/all
>
> Clean up the storage

**info**

[GET]

> http://localhost:5000/info
>
> Return a json {'number of images' : number of images , 'total size (Mb)' : total size in Mb}


## 4. License

MIT






