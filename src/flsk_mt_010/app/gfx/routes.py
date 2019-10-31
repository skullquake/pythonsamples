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
from PIL import ImageFilter
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
	#genvec()
	w=request.args.get('w',600,type=int)
	h=request.args.get('h',300,type=int)
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
	#print(rows.items[0])
	for r in rows.items:
		x=int(scale*(getattr(r,atx)-xmin))
		y=int(scale*(getattr(r,aty)-ymin))
		draw.line((x,y+csz)+(x,y-csz),fill=fill)
		draw.line((x+csz,y)+(x-csz,y),fill=fill)
		idx+=1
	del draw
	return serve_pil_image(im)
@bp.route('/plot3',methods=['GET'])
@login_required
def plot3():
	#genvec()
	w=request.args.get('w',600,type=int)
	h=request.args.get('h',300,type=int)
	t=request.args.get('tbl',default='Vec3F',type=str)
	atx=request.args.get('x',default='X',type=str)
	aty=request.args.get('y',default='Y',type=str)
	atz=request.args.get('z',default='Z',type=str)
	xmax=request.args.get('xmax',db.session.query(db.func.max(getattr(db.Model._decl_class_registry.get(t),atx))).scalar(),type=float)
	xmin=request.args.get('xmin',db.session.query(db.func.min(getattr(db.Model._decl_class_registry.get(t),atx))).scalar(),type=float)
	ymax=request.args.get('ymax',db.session.query(db.func.max(getattr(db.Model._decl_class_registry.get(t),aty))).scalar(),type=float)
	ymin=request.args.get('ymin',db.session.query(db.func.min(getattr(db.Model._decl_class_registry.get(t),aty))).scalar(),type=float)
	zmax=request.args.get('zmax',db.session.query(db.func.max(getattr(db.Model._decl_class_registry.get(t),atz))).scalar(),type=float)
	zmin=request.args.get('zmin',db.session.query(db.func.min(getattr(db.Model._decl_class_registry.get(t),atz))).scalar(),type=float)
	yoff=request.args.get('yoff',0,type=float)
	xoff=request.args.get('xoff',0,type=float)
	zoff=request.args.get('zoff',0,type=float)
	sx=request.args.get('sx',1,type=float)
	sy=request.args.get('sy',1,type=float)
	sz=request.args.get('sz',1,type=float)
	srch=abs(ymax-ymin)
	srcw=abs(xmax-xmin)
	srcd=abs(zmax-zmin)
	scale=min(w/srcw,h/srch)
	rows=db.Model._decl_class_registry.get(t).query.all()
	im=Image.new("RGB",(w,h),(0,0,0,0))
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
	csz=2
	imcros=Image.new("RGBA",(16,16),(0,0,0,0))
	imcrosdraw=ImageDraw.Draw(imcros,'RGBA')
	imcrosdraw.line((8,0,8,16),fill=(255,32,32,255))
	imcrosdraw.line((0,8,16,8),fill=(255,32,32,255))
	del imcrosdraw
	imcros=imcros.filter(ImageFilter.GaussianBlur(1))
	data=[]
	#print(rows.items[0])
	for r in rows:
		val=int(255*(getattr(r,atz)-zmin)/(zmax-zmin))
		fill=(255,32,32,128)#val)
		x=int(scale*(getattr(r,atx)-xmin))
		y=int(scale*(getattr(r,aty)-ymin))
		#im.alpha_composite(imcros,(x,y))
		draw.line((x,y+csz)+(x,y-csz),fill=fill)
		draw.line((x+csz,y)+(x-csz,y),fill=fill)
		idx+=1
	del draw
	return serve_pil_image(im)

@bp.route('/simplex',methods=['GET'])
@login_required
def simplex():
	w=256
	h=256
	s=OpenSimplex()
	im=Image.new("L",(w,h))
	for y in range(0,h):
		for x in range(0,w):
			val=s.noise2d(x,y)
			col=int(val+1)*128
			im.putpixel((x,y),col)
	return serve_pil_image(im)
class Biome:
	WATER=0
	BEACH=1
	FOREST=2
	JUNGLE=4
	SAVANNAH=5
	DESERT=6
	SNOW=7
def getBiome(a):
	if a<0.1:
		return Biome.WATER
	elif a<0.2:
		return Biome.BEACH
	elif a<0.3:
		return Biome.FOREST
	elif a<0.5:
		return Biome.JUNGLE
	elif a<0.7:
		return Biome.SAVANNAH
	elif a<0.9:
		return Biome.DESERT
	return Biome.SNOW
@bp.route('/noise',methods=['GET'])
@login_required
def noise():
	w=request.args.get('w',256,type=int)
	h=request.args.get('h',256,type=int)
	f=request.args.get('f',1,type=float)
	xoff=request.args.get('x',random.randint(0,1042),type=float)
	yoff=request.args.get('y',random.randint(0,1042),type=float)
	p=request.args.get('p',random.random(),type=float)
	l=request.args.get('l',0,type=int)
	b=request.args.get('b',random.random(),type=float)
	o=request.args.get('o',1,type=int)
	vpow=request.args.get('pow',1,type=float)
	im=Image.new("RGB",(w,h))
	vmin=None
	vmax=None
	for y in range(0,h):
		for x in range(0,w):
			#val=pnoise2(float(x),float(y),octaves=1,persistence=0.5,lacunarity=1,repeatx=w,repeaty=h,base=1)
			val=pnoise2(
				f*float(xoff+x),
				f*float(yoff+y),
				#f*(0.5+float(xoff+x)),
				#f*(0.5+float(yoff+y)),
				#octaves=int(o),
				#persistance=int(p),
				#lacunarity=l
			)
			val=math.pow(val,vpow) if val >0 else math.pow(-val,vpow)
			vmin=val if vmin==None else val if val<vmin else vmin
			vmax=val if vmax==None else val if val>vmin else vmin
			col=None
#			b=getBiome(val)
#			if b==Biome.WATER:
#				col=colorsys.hls_to_rgb(1.0,0.0,0.0)#(val,0,0)
#				#col=(4,4,4)
#			elif b==Biome.BEACH:
#				col=colorsys.hls_to_rgb(1.0,0.1,0.0)#(val,0,0)
#				#col=(8,8,8)
#			elif b==Biome.FOREST:
#				col=colorsys.hls_to_rgb(1.0,0.2,0.0)#(val,0,0)
#				#col=(16,16,16)
#			elif b==Biome.JUNGLE:
#				col=colorsys.hls_to_rgb(1.0,0.5,0.0)#(val,0,0)
#				#col=(32,32,32)
#			elif b==Biome.SAVANNAH:
#				col=colorsys.hls_to_rgb(1.0,0.6,0.0)#(val,0,0)
#				#col=(64,64,64)
#			elif b==Biome.DESERT:
#				col=colorsys.hls_to_rgb(1.0,0.7,0.0)#(val,0,0)
#				#col=(128,128,128)
#			elif b==Biome.SNOW:
#				col=colorsys.hls_to_rgb(0.9,0.9,0.0)#(val,0,0)
#				#col=(255,255,255)
			#col=colorsys.hls_to_rgb(abs(val),0.5,0.5)#(val,0,0)
			col=(int(val*255),int(val*255),int(val*255))
			#col=(int(col[0]*255),int(col[1]*255),int(col[2]*255))
			#print(val)
			im.putpixel((x,y),col)
	draw=ImageDraw.Draw(im,'RGBA')
	fnt=ImageFont.truetype("./res/ProggyClean.ttf",32)
#	draw.text(
#		(0,0),
#		'test',
#		font=fnt,
#		fill=(255,255,255,32)
#	)
	draw.multiline_text(
		(0,0),
		f"min:{vmin}\nmax:{vmax}",
		font=fnt,
		fill=(255,255,255,8),
		anchor=(0,0),
		align='left'
	)

	del draw

	return serve_pil_image(im)
@bp.route('/mpl',methods=['GET'])
def mpl():
	fig = mplfig()
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')
def mplfig():
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	xs = range(100)
	ys = [random.randint(1, 50) for x in xs]
	axis.plot(xs, ys)
	return fig
@bp.route('/mpl3d',methods=['GET'])
def mpl3d():
	matplotlib.rcParams['legend.fontsize'] = 10
	fig=Figure()
	ax=fig.gca(projection='3d')
	theta = numpy.linspace(-4 * numpy.pi, 4 * numpy.pi, 100)
	z = numpy.linspace(-2, 2, 100)
	r = z**2 + 1
	x = r * numpy.sin(theta)
	y = r * numpy.cos(theta)
	ax.plot(x, y, z, label='parametric curve')
	ax.legend()
	output=io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')




