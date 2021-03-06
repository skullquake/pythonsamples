import os
basedir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
	SECRET_KEY=os.environ.get('SECRET_KEY')or'you-will-never-guess'
	STATIC_FOLDER="app/static"
	STATIC_PATH='app/static'
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	#static_folder="web/static",
	#template_folder="web/templates"
