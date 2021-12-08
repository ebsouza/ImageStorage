# Image Storage 

Store images on remote machine using HTTP requests.

![](readme/ImageStorage_v2.gif)

(Icons made by Those Icons and catkuro from 'www.flaticon.com')

What could come next?

- Auth system;
- Cryptography;
- Async requests;
- gRPC;
- Image processing on Background jobs.


## 1. Turning on the server

You need an environment with Python 3.x and packages listed on requirements.txt file. 

1. Clone this project 
```shell
git clone https://github.com/ebsouza/ImageStorage.git
```

2. Enter into project folder
```shell
cd ImageStorage
```

3. Install packages listed on requirements.txt file
```shell
pip install -r requirements.txt
```

4. Setup environment variables
```shell
$ . instance/setup_production.sh
```

5. Run the API
```shell
$ python run.py
```


6. Make suer the server is turned on 
```shell
$ curl http://<host-ip>:5000/
```

'Image Storage API. By: EBSouza' should appear on the screen.



## 2. Test

Run all tests with test.py script.

```shell
$ python test.py
```


## 3. API Reference

See also some [examples](https://github.com/ebsouza/ImageStorage/tree/master/client).

#### Create an image

```http
  POST /image
```

```javascript
// payload
{ 
    "id": <image_id>,
    "image_data": <image.base64>
}
```


#### Get one image

```http
  GET /image/<image_id>
```

```javascript
// return
{ 
    [
        {
            "id": <image_id>,
            "image_data": <image.base64>
        }
    ]
}
```

#### Get all images

```http
  GET /image
```

```javascript
// return
{ 
    [
        {
            "id": <image_id>,
            "image_data": <image.base64>
        },
        {
            "id": <image_id>,
            "image_data": <image.base64>
        },
    ]
}
```

#### Delete one image

```http
  DELETE /image/<image_id>
```

#### Delete all images

```http
  DELETE /image
```

#### Recover system info

```http
  GET /info
```

```javascript
// return
{ 
    "total_images": 23,
    "total_size": 72.7
}
```


## 4. License

MIT






