import flask
from flask import\
	render_template,\
	flash,\
	redirect,\
	url_for,\
	request,\
	current_app
from flask_login import\
	current_user,\
	login_user,\
	logout_user,\
	login_required
from werkzeug.urls import\
	url_parse
from app import \
	db
from dateutil.parser import\
	parse
from flask_babel import \
	_
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

import requests
from app.gis import bp
import random
@bp.route('/gis',methods=['GET','POST'])
@login_required
def gis():
	return render_template(
		"gis.html"
	)
