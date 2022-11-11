import os
from flask import jsonify, request

from . import main as app
from instance.config import app_config

from .utils import get_total_images, get_total_size
from .model import remove_image, remove_images, decode_image, create_image, encode_image

app_settings = os.getenv('APP_SETTINGS', 'development')
path_to_images = app_config[app_settings][1]
image_extension = os.getenv('FILE_EXTENSION')

@app.route('/')
def about():
    return 'Image Storage API. By: EBSouza'


@app.route('/image', defaults={'image_id': ''})
@app.route('/image/<image_id>', methods=['GET'])
def get_image_view(image_id):
    image_ids = list()
    images = list()
    if not image_id:
        path, dirs, files = next(os.walk(path_to_images))
        image_ids = [image_id.rsplit(".", 1)[0] for image_id in files]
    else:
        image_ids.append(image_id)

    for image_id in image_ids:
        images.append({
                        "id": image_id,
                        "encoded_image": encode_image(image_id)
                      })

    return jsonify(images), 200


@app.route('/info', methods=['GET'])
def sys_info_view():
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


@app.route('/image', defaults={'image_id': ''}, methods=['DELETE'])
@app.route('/image/<image_id>', methods=['DELETE'])
def remove_image_view(image_id):
    try:
        if not image_id:
            removed = remove_images()
        else:
            removed = remove_image(image_id)

        return {'data': removed}, 200
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        return error_message, 500
