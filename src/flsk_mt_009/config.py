import os
basedir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
	SECRET_KEY=os.environ.get('SECRET_KEY')or'you-will-never-guess'
	STATIC_FOLDER="app/static"
	STATIC_PATH='app/static'
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	ADMINS=['ockert8080@gmail.com']
	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=587
	MAIL_USE_TLS=1
	MAIL_USERNAME='ockert8080@gmail.com'
	MAIL_PASSWORD=''
	POSTS_PER_PAGE=5
	LANGUAGES=['en','es']
