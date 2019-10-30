from flask import\
	Flask,\
	request
from config import\
	Config
from flask_sqlalchemy import\
	SQLAlchemy
from flask_migrate import\
	Migrate
from flask_login import\
	LoginManager
import logging
from logging.handlers import\
	SMTPHandler,\
	RotatingFileHandler
from flask_mail import\
	Mail
from flask_moment import\
	Moment
from flask_babel import\
	Babel
import os
import flask_excel as excel
db=SQLAlchemy()
migrate=Migrate()
login=LoginManager()
login.login_view='auth.login'
mail=Mail()
moment=Moment()
babel=Babel()
@babel.localeselector
def get_locale():
	#return request.accept_languages.best_match(app.config['LANGUAGES'])
	return 'af'
def create_app(config_class=Config):
	print('----------------------------------------')
	print('CREATING APPLICATION')
	print('----------------------------------------')
	#app=Flask(__name__)
	app=Flask(
		__name__,
		static_url_path="/",
		template_folder="templates"
	)
	app.config.from_object(config_class)
	db.init_app(app)
	migrate.init_app(app,db)
	login.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	babel.init_app(app)
	excel.init_excel(app) # required since version 0.0.7
	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)
	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp,url_prefix='/auth')
	from app.main import bp as main_bp
	app.register_blueprint(main_bp)
	from app.gis import bp as gis_bp
	app.register_blueprint(gis_bp,url_prefix='/gis')
	from app.d3 import bp as d3_bp
	app.register_blueprint(d3_bp,url_prefix='/d3')
	from app.gfx import bp as gfx_bp
	app.register_blueprint(gfx_bp,url_prefix='/gfx')
	from app.excel import bp as excel_bp
	app.register_blueprint(excel_bp,url_prefix='/excel')
	from app.hr import bp as hr_bp
	app.register_blueprint(hr_bp,url_prefix='/hr')
	if not app.debug:
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,backupCount=10)
		file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)
		app.logger.setLevel(logging.INFO)
		app.logger.info('Microblog startup')
	return app
