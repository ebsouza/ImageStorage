import os
import base64
from flask import jsonify, abort, request

from instance.config import app_config
from . import main as app

from .utils import get_total_images, get_total_size
from .model import remove_image, remove_images, decode_image, create_image

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
    try:
        data = dict()
        absolute_path = os.path.abspath(path_to_images)
        data['total_images'] = get_total_images(absolute_path)
        data['total_size'] = get_total_size(absolute_path)
        return jsonify(data), 200

    except Exception as e:
        error_message = f"Unexpected error: {e}"
        return error_message, 500


@app.route('/image', methods=['POST'])
def create_image_view():
    try:
        image_64_encode = request.get_json()['image_data']
        image_64_decoded = decode_image(image_64_encode)
        image_id = request.get_json()['id']

        create_image(image_id, image_64_decoded)

        return {'data': image_id}, 201

    except Exception as e:
        error_message = f"Unexpected error: {e}"
        return error_message, 500


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
