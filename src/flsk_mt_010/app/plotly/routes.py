import os
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
	jsonify,\
	send_file
from flask_login import\
	login_required
from werkzeug.urls import\
	url_parse
from app import \
	db
from app.plotly import bp
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go
@bp.route('/home',methods=['GET'])
@login_required
def home():
	bar=create_plot()
	return render_template(
		"plotly/home.html",
		plot=bar
	)
def create_plot():
	N=40
	x=np.linspace(0,1,N)
	y=np.random.randn(N)
	df=pd.DataFrame({'x':x,'y':y})
	data=[
		go.Bar(
			x=df['x'],
			y=df['y']
		)
	]
	graphJSON=json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON
