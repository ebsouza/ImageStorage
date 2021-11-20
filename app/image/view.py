import os
import base64
from flask import jsonify, abort, request

from instance.config import app_config
from . import main as app

from .model import remove_image, remove_images

app_settings = os.getenv('APP_SETTINGS', 'development')
path_to_images = app_config[app_settings][1]
image_extension = os.getenv('FILE_EXTENSION')


@app.route('/')
def about():
    return 'Image Storage API. By: EBSouza'


@app.route('/image/<image_id>', methods=['GET'])
def get_image_list(image_id):
    if image_id == "all":
        image_list = []

        try:
            print(path_to_images)
            path, dirs, files = next(os.walk(path_to_images))
        except Exception as e:
            error = 'Failed to access directory.'
            print(error + 'Reason: %s' % (e))
            return error, 500

        if len(files) == 0:
            return 'No image in storage', 404

        for file in files:
            image_info = {}
            image_info['file_name'] = file
            filePath = path_to_images + file
            mb = os.stat(filePath).st_size / 1000000
            image_info['size (Mb)'] = mb
            image_list.append(image_info)

        return jsonify(image_list), 200
    else:

        json_file = {}
        json_file['ID'] = image_id

        try:
            image = open(path_to_images + image_id + image_extension, 'rb')
        except Exception as e:
            error = 'Unexpected error: Failed to open the image.'
            print(error + 'Reason: %s' % (e))
            return error, 500

        image_read = image.read()
        image_64_encode = base64.encodestring(image_read)
        image_64_encode = image_64_encode.decode("utf-8")

        json_file['image_data'] = image_64_encode

        return jsonify(json_file), 200


@app.route('/info', methods=['GET'])
def sys_info():
    # INFO
    # --nFiles
    try:
        path, dirs, files = next(os.walk(path_to_images))
    except Exception as e:
        error = 'Failed to access directory.'
        print(error + 'Reason: %s' % (e))
        return error, 500

    nFiles = len(files)

    # --size
    totalSize = 0
    for file in files:
        filePath = path_to_images + file
        totalSize += os.stat(filePath).st_size
    totalSize = totalSize / 1000000  # convert to Mb

    payload = {}
    payload['number of images'] = nFiles
    payload['total size (Mb)'] = totalSize

    return jsonify(payload), 200


@app.route('/image', methods=['POST'])
def set_image():
    file_json = {}

    # Load JSON
    try:
        file_json = request.get_json()
    except Exception as e:
        error = 'Cant open Json.'
        print(error + 'Reason: %s' % (e))
        return error, 400

    # Check wheter Json is empty
    if file_json == {}:
        return 'Json is empty', 400

    # Decode image
    try:
        image_64_encode = request.get_json()['image_data']
        image_64_encode = image_64_encode.encode("utf-8")
        # image_64_decode = base64.decodestring(image_64_encode) #Deprecated
        image_64_decode = base64.decodebytes(image_64_encode)
    except Exception as e:
        error = 'Invalid data on Json.'
        print(error + 'Reason: %s' % (e))
        return error, 400

    # Write the image
    try:
        image_path = path_to_images + request.get_json()['ID'] + image_extension

        with open(image_path, 'wb') as image_result:
            image_result.write(image_64_decode)

    except Exception as e:
        error = 'Unexpected error: Failed to create image.'
        print(error + 'Reason: %s' % (e))
        return error, 500

    return 'Image has been created.', 201


@app.route('/image/<image_id>', methods=['DELETE'])
def remove_image_view(image_id):
    try:
        if image_id == "all":
            removed = remove_images()
        else:
            removed = remove_image(image_id)

        return {'data': removed}, 200
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        return error_message, 500
