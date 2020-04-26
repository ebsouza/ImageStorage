import os

from app import create_app

#config_name = os.getenv('APP_SETTINGS') # config_name = "development"
config_name = 'production'
image_extension = '.jpg'
app = create_app(config_name, image_extension)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)