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
from app.d3 import bp
import random
import json
#@bp.route('/linechart/<t>/<a>',methods=['GET'],defaults={'t':'Mag','a':'BT'})
@bp.route('/linechart',methods=['GET'])
@login_required
def linechart():
	t=request.args.get('t',default='Mag',type=str)
	a=request.args.get('a',default='BT',type=str)
	return render_template(
		"d3.html",
		table=t,
		attr=a,
	)
#@bp.route('/d3/data/<t>/<a>',methods=['GET'],defaults={'t':'Mag','a':'BT'})
@bp.route('/data',methods=['GET'])
def d3data():
	t=request.args.get('t',default='Mag',type=str)
	a=request.args.get('a',default='BT',type=str)
	res=flask.Response()
	res.headers['Content-type']='application/json'
	rows=db.Model._decl_class_registry.get(t).query.order_by(db.Model._decl_class_registry.get(t).id.desc()).paginate(
		1,
		4096,
		False
	)
	data=[]
	for r in rows.items:#range(1,32):
		data.append(
			{
				"xVal": r.id,
				"yVal": getattr(r,a)
			}
		)
	res.set_data(json.dumps(data))
	return res
