from flask import Flask, jsonify, abort, request, make_response, url_for
import base64
import os
import json
from PIL import Image 

from instance.config import app_config

#Possible extensions
image_extension_list = ['.jpg', '.png', '.jpeg']

def create_app(config_name, image_extension):

    #Server configs
    app = Flask(__name__)
    app.config.from_object(app_config[config_name][0])

    #Path to images
    path_to_images = app_config[config_name][1]
    
    #Check extension validity
    if image_extension not in image_extension_list:
        raise NameError('Extension is not valid.')

    @app.route('/')
    def about():
        return 'Image Storage API. By: Erick Barbosa'


    # --- GET Methods
    @app.route('/image/<image_id>', methods = ['GET'])
    def get_image_list(image_id):
        if image_id == "all":
            image_list = []

            try:
                print(path_to_images)
                path, dirs, files = next(os.walk( path_to_images ))
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

            return jsonify( image_list ), 200
        else:
            
            json_file = {}
            json_file['ID'] = image_id

            try:
                image = open( path_to_images + image_id + image_extension, 'rb') 
            except Exception as e:
                error = 'Unexpected error: Failed to open the image.'
                print(error + 'Reason: %s' % (e))
                return error, 500

            image_read = image.read() 
            image_64_encode = base64.encodestring(image_read) 
            image_64_encode = image_64_encode.decode("utf-8")

            json_file['image_data'] = image_64_encode

            return jsonify(json_file), 200


    @app.route('/info', methods = ['GET'])
    def sys_info():

        #INFO
        #--nFiles
        try:
            path, dirs, files = next(os.walk( path_to_images ))
        except Exception as e:
            error = 'Failed to access directory.'
            print(error + 'Reason: %s' % (e))
            return error, 500

        nFiles = len(files)

        #--size
        totalSize = 0
        for file in files:
            filePath = path_to_images + file
            totalSize += os.stat(filePath).st_size
        totalSize = totalSize/1000000 #convert to Mb

        payload = {}
        payload['number of images'] = nFiles
        payload['total size (Mb)'] = totalSize

        return jsonify( payload ), 200

    # --- POST Methods
    @app.route('/image', methods = ['POST'])
    def set_image():

        file_json = {}

        #Load JSON
        try:
            file_json = request.get_json()
        except Exception as e:
            error = 'Cant open Json.'
            print(error + 'Reason: %s' % (e))
            return error, 400

        #Check wheter Json is empty
        if file_json == {}:
            return 'Json is empty', 400

        #Decode image
        try:
            image_64_encode = request.get_json()['image_data']
            image_64_encode = image_64_encode.encode("utf-8")
            #image_64_decode = base64.decodestring(image_64_encode) #Deprecated
            image_64_decode = base64.decodebytes(image_64_encode) 
        except Exception as e:
            error = 'Invalid data on Json.'
            print(error + 'Reason: %s' % (e))
            return error, 400

        #Write the image
        try:  
            image_path = path_to_images + request.get_json()['ID'] + image_extension

            with open(image_path, 'wb') as image_result:
                image_result.write(image_64_decode)

        except Exception as e:
            error = 'Unexpected error: Failed to create image.'
            print(error + 'Reason: %s' % (e))
            return error, 500

        return 'Image has been created.', 201


    # --- DELETE Methods
    @app.route('/image/<image_id>', methods = ['DELETE'])
    def remove_image(image_id):

        try:
            if ( image_id == "all" ):
                for filename in os.listdir(path_to_images):
                    file_path = os.path.join(path_to_images, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                        abort(400)
            else: 
                #Delete specified image ( Adicionar try/except )
                os.remove( path_to_images + image_id + image_extension )
        except:
            return 'Unexpected error', 500

        return 'OK', 200


    return app






