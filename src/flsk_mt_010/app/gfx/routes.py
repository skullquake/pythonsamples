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
from app.gfx import bp
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

@bp.route('/home',methods=['GET'])
@login_required
def home():
	return render_template(
		"gfx.html"
	)
@bp.route('/line',methods=['GET'])
@login_required
def line():
	w=request.args.get('w',1600,type=int)
	h=request.args.get('h',500,type=int)
	im=Image.new("RGB",(w,h))
	draw=ImageDraw.Draw(im,'RGBA')
	t=request.args.get('tbl',default='Mag',type=str)
	a=request.args.get('atr',default='BT',type=str)
	#rows=db.Model._decl_class_registry.get(t).query.order_by(db.Model._decl_class_registry.get(t).id.desc()).paginate(
	rows=db.Model._decl_class_registry.get(t).query.paginate(
		1,
		w,
		False
	)
	valmax=request.args.get('max',db.session.query(db.func.max(getattr(db.Model._decl_class_registry.get(t),a))).scalar(),type=float)
	valmin=request.args.get('min',db.session.query(db.func.min(getattr(db.Model._decl_class_registry.get(t),a))).scalar(),type=float)
	valcmx=request.args.get('cmx',9999.99,type=float)
	valcmn=request.args.get('cmn',-9999.99,type=float)
	if valmax>valcmx:
		valmax=valcmx
	if valmin<valcmn:
		valmin=valcmn
	data=[]
	for y in range(0,h,1):
		draw.line(
			(0,y)+(w,y),
			fill="hsl({}, {}%, {}%)".format(8,100,16-y/h*16)
		)
	for y in range(0,h,8):
		draw.line(
			(0,y)+(w,y),
			fill="hsl({}, {}%, {}%)".format(8,100,8)
		)
	for x in range(0,w,8):
		draw.line(
			(x,0)+(x,h),
			fill="hsl({}, {}%, {}%)".format(8,100,8)
		)
	idx=0
	for r in rows.items:
		y=int(h-h*(float(getattr(r,a))-valmin)/abs(valmax-valmin))
		if float(getattr(r,a))>valcmn and float(getattr(r,a))<valcmx:
			draw.line(
				(
					idx,
					h
				)
				+
				(
					idx,
					y
					
				),
				#fill="hsl({}, {}%, {}%)".format(r.id,255,255)
				#fill=(255,255,255,255)
				fill=(255,32,32,int(255*getattr(r,a)/valmax))
			)
		idx+=1
	del draw
	return serve_pil_image(im)
@bp.route('/plot',methods=['GET'])
@login_required
def plot():
	w=request.args.get('w',800,type=int)
	h=request.args.get('h',800,type=int)
	t=request.args.get('tbl',default='Vec2F',type=str)
	atx=request.args.get('x',default='X',type=str)
	aty=request.args.get('y',default='Y',type=str)
	xmax=request.args.get('xmax',db.session.query(db.func.max(getattr(db.Model._decl_class_registry.get(t),atx))).scalar(),type=float)
	xmin=request.args.get('xmin',db.session.query(db.func.min(getattr(db.Model._decl_class_registry.get(t),atx))).scalar(),type=float)
	ymax=request.args.get('ymax',db.session.query(db.func.max(getattr(db.Model._decl_class_registry.get(t),aty))).scalar(),type=float)
	ymin=request.args.get('ymin',db.session.query(db.func.min(getattr(db.Model._decl_class_registry.get(t),aty))).scalar(),type=float)
	yoff=request.args.get('yoff',0,type=float)
	xoff=request.args.get('xoff',0,type=float)
	sx=request.args.get('sx',1,type=float)
	sy=request.args.get('sy',1,type=float)
	srch=abs(ymax-ymin)
	srcw=abs(xmax-xmin)
	scale=min(w/srcw,h/srch)
	rows=db.Model._decl_class_registry.get(t).query.paginate(
		1,
		4096,
		False
	)
	im=Image.new("RGB",(w,h))
	draw=ImageDraw.Draw(im,'RGBA')
	data=[]
	for y in range(0,h,1):
		draw.line(
			(0,y)+(w,y),
			fill="hsl({}, {}%, {}%)".format(0,100,16-y/h*16)
		)
	for y in range(0,h,8):
		draw.line(
			(0,y)+(w,y),
			fill="hsl({}, {}%, {}%)".format(8,100,8)
		)
	for x in range(0,w,8):
		draw.line(
			(x,0)+(x,h),
			fill="hsl({}, {}%, {}%)".format(8,100,8)
		)
	idx=0
	fill=(255,32,32,255)
	csz=2
	for r in rows.items:
		x=int(scale*(getattr(r,atx)))
		y=int(scale*(getattr(r,aty)))
		#print(f"{x}:{y}")
		draw.line((x,y+csz)+(x,y-csz),fill=fill)
		draw.line((x+csz,y)+(x-csz,y),fill=fill)
		idx+=1
	del draw
	return serve_pil_image(im)
def serve_pil_image(pil_img):
	#img_io = StringIO()
	img_io = BytesIO()
	#pil_img.save(img_io, 'JPEG', quality=70)
	pil_img.save(img_io, 'PNG')
	img_io.seek(0)
	#return send_file(img_io, mimetype='image/jpeg')
	return send_file(img_io, mimetype='image/png')
