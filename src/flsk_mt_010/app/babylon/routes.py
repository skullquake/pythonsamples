import io
from io import\
	StringIO,\
	BytesIO
import flask
from flask import\
	render_template,\
	flash,\
	redirect,\
	url_for,\
	request,\
	current_app,\
	send_file
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
from sqlalchemy import\
	create_engine,\
	func
from sqlalchemy import MetaData
from sqlalchemy import Table

import requests
from app.babylon import bp
import random
import json
import io
from PIL import ImageChops
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont
import os
import random 
import math
from opensimplex import\
	OpenSimplex
from noise import\
	pnoise2
import colorsys
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib.pyplot
import urllib


def serve_pil_image(pil_img):
	#img_io = StringIO()
	img_io = BytesIO()
	#pil_img.save(img_io, 'JPEG', quality=70)
	pil_img.save(img_io, 'PNG')
	img_io.seek(0)
	#return send_file(img_io, mimetype='image/jpeg')
	return send_file(img_io, mimetype='image/png')
def genvec():
	_min=-8
	_max=8
	db.session.query(db.Model._decl_class_registry.get('Vec2F')).delete()
	db.session.commit()
	for a in range(1024):
		b=db.Model._decl_class_registry.get('Vec2F')(
			X=random.random()*(abs(_min-_max))+_min,
			Y=random.random()*(abs(_min-_max))+_min
		)
		db.session.add(b)
	db.session.commit()
@bp.route('/home',methods=['GET'])
@login_required
def home():
	return render_template(
		"babylon.html",
		args=request.args
	)

