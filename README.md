# Image Storage 

Store images on remote machine using HTTP requests.

![](readme/ImageStorage_v2.gif)

(Icons made by Those Icons and catkuro from 'www.flaticon.com')


## 1. Starting Image Storage

```shell
docker-compose up
```

Checking everything is ok

```shell
$ curl http://<host-ip>:5000/
```

'Image Storage API. By: EBSouza' should appear for you.

## 1.1 Testing

```shell
docker exec -it <container-name> bash -c "python test.py"
```

## 2. API Reference

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


## 3. License

MIT
