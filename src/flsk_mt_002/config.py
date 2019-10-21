import os
class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY')or'you-will-never-guess'
    STATIC_FOLDER="app/static"
    STATIC_PATH = 'app/static'
    #static_folder="web/static",
    #template_folder="web/templates"

