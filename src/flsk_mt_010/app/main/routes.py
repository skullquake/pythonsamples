import flask
from flask import\
	render_template,\
	flash,\
	redirect,\
	url_for,\
	request,\
	current_app
#from app import\
#	app
from app.main.forms import\
	EditProfileForm,\
	PostForm,\
	AjaxTestForm
from flask_login import\
	current_user,\
	login_user,\
	logout_user,\
	login_required
from app.models import\
	User,\
	Post,\
	Trajectory,\
	Cpu
from werkzeug.urls import\
	url_parse
from app import \
	db
from datetime import\
	datetime
from dateutil.parser import\
	parse
from flask_babel import \
	_
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

import psutil
import sys
import json
import time
import requests
from app.main import bp
@bp.route('/')
@bp.route('/index',methods=['GET','POST'])
@login_required
def index():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(body=form.post.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(_('Your post is now live!'))
		return redirect(url_for('main.index'))
	page=request.args.get(
		'page',
		1,
		type=int
	)
	posts=current_user.followed_posts().paginate(
		page,
		current_app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('main.index',page=posts.next_num)if posts.has_next else None
	prev_url=url_for('main.index',page=posts.prev_num)if posts.has_prev else None
	return render_template(
		"index.html",
		title='Home Page',
		form=form,
		posts=posts.items,
		next_url=next_url,
		prev_url=prev_url
	)
@bp.route('/users')
@login_required
def users():
	page=request.args.get(
		'page',
		1,
		type=int
	)
	users=User.query.paginate(
		page,
		current_app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('main.users',page=users.next_num)if users.has_next else None
	prev_url=url_for('main.users',page=users.prev_num)if users.has_prev else None
	return render_template(
		'users.html',
		users=users.items,
		next_url=next_url,
		prev_url=prev_url
	)
@bp.route('/user/<username>')
@login_required
def user(username):
	user=User.query.filter_by(username=username).first_or_404()
	posts=[
		{'author':user,'body':'Test post #1'},
		{'author':user,'body':'Test post #2'}
	]
	page=request.args.get(
		'page',
		1,
		type=int
	)
	posts=user.posts.order_by(Post.timestamp.desc()).paginate(
		page,
		current_app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('user',username=user.username,page=posts.next_num)if posts.has_next else None
	prev_url=url_for('user',username=user.username,page=posts.prev_num)if posts.has_prev else None
	return render_template(
		'user.html',
		user=user,
		posts=posts.items,
		next_url=next_url,
		prev_url=prev_url,
	)
@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
@bp.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form=EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username=form.username.data
		current_user.about_me=form.about_me.data
		db.session.commit()
		flash(_('Your changes have been saved.'))
		return redirect(url_for('edit_profile'))
	elif request.method=='GET':
		form.username.data=current_user.username
		form.about_me.data=current_user.about_me
	return render_template('edit_profile.html',title='Edit Profile',form=form)
@bp.route('/follow/<username>')
@login_required
def follow(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.',username=username))
		return redirect(url_for('main.index'))
	if user==current_user:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('user',username=username))
	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(username)s!',username=username))
	return redirect(url_for('user',username=username))
@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.',username=username))
		return redirect(url_for('main.index'))
	if user==current_user:
		flash(_('You cannot unfollow yourself!'))
		return redirect(url_for('user',username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash(_('You are not following %(username)s.',username=username))
	return redirect(url_for('user', username=username))
@bp.route('/explore')
@login_required
def explore():
	page=request.args.get(
		'page',
		1,
		type=int
	)
	posts=Post.query.order_by(
		Post.timestamp.desc()
	).paginate(
		page,current_app.config['POSTS_PER_PAGE'],
		False
	)
	page=request.args.get(
		'page',
		1,
		type=int
	)
	posts=Post.query.order_by(Post.timestamp.desc()).paginate(
		page,
		current_app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('main.explore',page=posts.next_num)if posts.has_next else None
	prev_url=url_for('main.explore',page=posts.prev_num)if posts.has_prev else None
	return render_template(
		'index.html',
		title='Explore',
		posts=posts.items,
		next_url=next_url,
		prev_url=prev_url
	)
@bp.route('/trajectories')
@login_required
def trajectories():
	page=request.args.get(
		'page',
		1,
		type=int
	)
	trajectories=Trajectory.query.paginate(
		page,
		10,#current_app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('main.trajectories',page=trajectories.next_num)if trajectories.has_next else None
	prev_url=url_for('main.trajectories',page=trajectories.prev_num)if trajectories.has_prev else None
	return render_template(
		'trajectories.html',
		trajectories=trajectories.items,
		next_url=next_url,
		prev_url=prev_url
	)

@bp.route('/cpu', methods=['GET'])
@login_required
def cpu():
	headings=[]
	for a in Cpu.__table__.columns:
		headings.append(a.name)
	page=request.args.get(
		'page',
		1,
		type=int
	)
	rows=Cpu.query.order_by(Cpu.ts.desc()).paginate(
		page,
		10,#current_app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('main.cpu',page=rows.next_num)if rows.has_next else None
	prev_url=url_for('main.cpu',page=rows.prev_num)if rows.has_prev else None
	return render_template(
		'cpu.html',
		headings=headings,
		rows=rows.items,
		next_url=next_url,
		prev_url=prev_url
	)
@bp.route('/cpu', methods=['POST'])
def cpu_post():
	try:
		print(json.dumps(request.get_json(),indent=4))
		c=Cpu(
			ts=parse(request.get_json()['ts']),
			cpu=request.get_json()['main.cpu']
		)
		db.session.add(c)
		db.session.commit()
	except Exception as E:
		print(E)
	#print(request.get_json()['main.cpu'])
	return {'msg':'ok'}
@bp.route('/psutil', methods=['GET'])
@login_required
def _psutil():
	disks=[];
	i=0
	for disk in psutil.disk_partitions():
		diskobj=disk._asdict()
		diskobj["usage"]=psutil.disk_usage(i)._asdict()
		disks.append(diskobj)
	procs=[];
	for proc in psutil.process_iter():
		_proc={}
		_proc['cmdline']=proc.cmdline()
		_proc['create_time']=proc.create_time()
		_proc['is_running']=proc.is_running()
		_proc['cpu_percent']=proc.cpu_percent()
		#_proc['connections']=proc.connections()
		_proc['cwd']=proc.cwd()
		_proc['memory_percent']=proc.memory_percent()
		_proc['num_threads']=proc.num_threads()
		#_proc['parent']=proc.parent()
		_proc['pid']=proc.pid
		_proc['username']=proc.username()
		#_proc['open_files']=proc.open_files()
		procs.append(_proc)
		#procs.append(proc.cmdline())
	psdat=json.dumps(
		{
			'cpu_percent': psutil.cpu_percent(),
			'memory_percent': psutil.virtual_memory().percent,
			'cache_percent': psutil.virtual_memory().cached / psutil.virtual_memory().total * 100,
			'swap_percent': psutil.swap_memory().percent,
			'disk_percent': psutil.disk_usage('/').percent,
			#'bytes_in': bytes_in - bytes_in_last,
			#'bytes_out': bytes_out - bytes_out_last,
			'net_fds': len(psutil.net_connections()),
			'pids': len(psutil.pids()),
			'boot_time':psutil.boot_time(),
			'cpu_count':psutil.cpu_count(),
			'cpu_stats':psutil.cpu_stats(),
			'cpu_times':psutil.cpu_times(),
			'cpu_times_percent':psutil.cpu_times_percent(),
			'disk_io_counters':psutil.disk_io_counters(),
			'disk_partitions':psutil.disk_partitions(),
			'getloadavg':psutil.getloadavg(),
			'net_if_addrs':psutil.net_if_addrs(),
			'net_if_stats':psutil.net_if_stats(),
			'net_io_counters':psutil.net_io_counters(),
			'pids':psutil.pids(),
			'sensors_battery()':psutil.sensors_battery(),
			'sensors_fans':psutil.sensors_fans(),
			'sensors_temperatures':psutil.sensors_temperatures(),
			#'swap_memory':psutil.swap_memory(),
			'virtual_memory':psutil.virtual_memory(),
			#'wait_procs':psutil.wait_procs(),
			#'cpu_freq':psutil.cpu_freq(),
			'procs':procs,
			'disks':disks
		},
		sort_keys=True,
		indent=4
	)
	return render_template(
		'psutil.html',
		psutil=psdat
	)
@bp.route('/tables', methods=['GET'])
@login_required
def tables():
#	tables=[]
#	m=MetaData()
#	m.reflect(db.engine)
#	_tables=m.tables
#	for t in _tables:
#		table={}
#		table['name']=_tables[t].name
#		table['cols']=[]
#		for c in _tables[t].columns:
#			table['cols'].append(c.name)
#		tables.append(table)
	tables=[]
	db.metadata.reflect(db.engine)
	for t in db.Model._decl_class_registry.values():
		try:
			table={}
			table['name']=t.__name__
			table['cols']=t.__table__.columns.keys()
			table['count']=db.session.query(t).count()
			tables.append(table)
		except Exception as E:
			print(str(E))		
	table={}
	table['name']='----'
	table['cols']=[]
	table['count']='---'
	tables.append(table)
	for t in db.metadata.tables:
		try:
			db.metadata.tables[t]
			table={}
			table['name']=db.metadata.tables[t].name
			table['cols']=[]
			for col in db.metadata.tables[t].columns:
				table['cols'].append(col.name)
			table['count']=0
			tables.append(table)
		except Exception as E:
			print(str(E))		
	return render_template(
		'tables.html',
		tables=tables
	)
@bp.route('/show_table/<tablename>',methods=['GET'])
@login_required
def show_table(tablename):
	headings=[]
	for a in db.Model._decl_class_registry.get(tablename).__table__.columns:
		headings.append(a.name)
	page=request.args.get(
		'page',
		1,
		type=int
	)
	rows=db.Model._decl_class_registry.get(tablename).query.paginate(
		page,
		10,
		False
	)
	next_url=url_for('main.show_table',tablename=tablename,page=rows.next_num)if rows.has_next else None
	prev_url=url_for('main.show_table',tablename=tablename,page=rows.prev_num)if rows.has_prev else None
	return render_template(
		'table.html',
		tablename=tablename,
		headings=headings,
		rows=rows.items,
		next_url=next_url,
		prev_url=prev_url
	)
@bp.route('/show_row/<tablename>/<rowid>',methods=['GET'])
@login_required
def show_row(tablename,rowid):
	headings=[]
	for a in db.Model._decl_class_registry.get(tablename).__table__.columns:
		headings.append(a.name)
	row=db.Model._decl_class_registry.get(tablename).query.filter_by(id=rowid).first()
	return render_template(
		'row.html',
		row=row,
		headings=headings
	)
@bp.route('/ajaxtest',methods=['GET'])
@login_required
def ajaxtest():
	form=AjaxTestForm()
	if form.validate_on_submit():
		flash(_('Your changes have been saved.'))
		return redirect(url_for('ajaxtest'))
	#elif request.method=='GET':
		#form.foo='test'
	return render_template(
		'ajaxtest.html',
		form=form
	)
@bp.route('/rest',methods=['GET'])
def rest_get():
	print('rest_get')
	res=flask.Response()
	res.headers['Content-type'] = 'application/json'
	try:
		hdr={'Content-type':'application/json'}
		dat={'qwer':'asdf'}
		req=requests.post('http://localhost:5000/rest',headers=hdr,data=dat)
		res.set_data(json.dumps({"msg":json.loads(req.content)}))
	except Exception as E:
		res.set_data(json.dumps({"err":str(E)}))
	return res
@bp.route('/rest',methods=['POST'])
def rest_post():
	print('rest_post')
	r=flask.Response()
	r.headers['Content-type'] = 'application/json'
	#return resp
	try:
		rjsonrequest.get_json();
	except Exception as E:
		r.set_data(json.dumps({"err":str(E)}))
	r.set_data(json.dumps({"msg":"post ok"}))
	return r




#for o in db.Model._decl_class_registry.values():
#...:	 try:
#...:		 r=o.query.all()
#...:	 except Exception as E:
#...:		 print(E)
#...:
#...:
# db.Model._decl_class_registry.get('Post')
#Trajectory.__table__.columns.keys()
#url_for('table', tablename=tablename) 
#----------------------------------------
#from sqlalchemy import Table
#from sqlalchemy import MetaData
#m=MetaData()
#t=Table('User',m,autoload_with=db.engine)
#for col in t.columns:
#	print(col)
#for tbl in m.tables:
#	print(tbl)
##metadata m will be incrementally extended with Table calls
#t=Table('Post',m,autoload_with=db.engine)
#for col in t.columns:
#	print(col)
#for tbl in m.tables:
#	print(m.tables[tbl].name)
#	print(m.tables[tbl].fullname)
#	for col in m.tables[tbl].columns:
#		print(col)
#----------------------------------------
#from sqlalchemy import MetaData
#from sqlalchemy import Table
#from sqlalchemy import Column
#from sqlalchemy import Integer
#t=Table('words',db.metadata,Column('id',Integer,primary_key=True)
#t.create(db.engine)
#----------------------------------------
#from sqlalchemy import Integer
#from sqlalchemy import String
#from sqlalchemy import Float
#class Test1(db.Model):
#	id=db.Column(db.Integer,primary_key=True)	
#class Test2(db.Model):
#	id=db.Column(db.Integer,primary_key=True)	
#	name=db.Column(db.String)
#class Test3(db.Model):
#	id=db.Column(db.Integer,primary_key=True)	
#	name=db.Column(db.String)
#	val=db.Column(db.Float)
#----------------------------------------
#after restart to get at the dynamically created stuff
#from sqlalchemy import MetaData
#m=MetaData()
#m.reflect(db.engine)
#print(list(m.tables))
#----------------------------------------
#inspector
#from sqlalchemy import inspector
#print(inspect(db.engine).get_table_names())
#for tblnam in inspect(db.engine).get_table_names():
#	print(inspect(db.engine).get_columns(tblnam))
#----------------------------------------
#select
#for a in db.metadata.tables['user'].select().execute():
#	print(a)
#----------------------------------------
#example request[s]
#----------------------------------------
#import requests
#auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}
#r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc/Translate?text={}&from={}&to={}'.format(text, source_language, dest_language),headers=auth)

