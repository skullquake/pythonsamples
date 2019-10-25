from flask import\
	render_template,\
	flash,\
	redirect,\
	url_for,\
	request
from app import\
	app
from app.forms import\
	LoginForm,\
	RegistrationForm,\
	EditProfileForm,\
	PostForm
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
from app.forms import\
	ResetPasswordRequestForm,\
	ResetPasswordForm
from app.email import\
	send_password_reset_email
from flask_babel import \
	_
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

import psutil
import sys
import json
import time
@app.route('/')
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(body=form.post.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(_('Your post is now live!'))
		return redirect(url_for('index'))
	page=request.args.get(
		'page',
		1,
		type=int
	)
	posts=current_user.followed_posts().paginate(
		page,
		app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('index',page=posts.next_num)if posts.has_next else None
	prev_url=url_for('index',page=posts.prev_num)if posts.has_prev else None
	return render_template(
		"index.html",
		title='Home Page',
		form=form,
		posts=posts.items,
		next_url=next_url,
		prev_url=prev_url
	)
@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(_('Invalid username or password'))
			return redirect(url_for('login'))
		login_user(user,remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
@app.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_('Congratulations, you are now a registered user!'))
		return redirect(url_for('login'))
	return render_template(
		'register.html',
		title='Register',
		form=form
	)
@app.route('/users')
@login_required
def users():
	page=request.args.get(
		'page',
		1,
		type=int
	)
	users=User.query.paginate(
		page,
		app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('users',page=users.next_num)if users.has_next else None
	prev_url=url_for('users',page=users.prev_num)if users.has_prev else None
	return render_template(
		'users.html',
		users=users.items,
		next_url=next_url,
		prev_url=prev_url
	)
@app.route('/user/<username>')
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
		app.config['POSTS_PER_PAGE'],
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
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
@app.route('/edit_profile',methods=['GET','POST'])
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
@app.route('/follow/<username>')
@login_required
def follow(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.',username=username))
		return redirect(url_for('index'))
	if user==current_user:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('user',username=username))
	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(username)s!',username=username))
	return redirect(url_for('user',username=username))
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.',username=username))
		return redirect(url_for('index'))
	if user==current_user:
		flash(_('You cannot unfollow yourself!'))
		return redirect(url_for('user',username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash(_('You are not following %(username)s.',username=username))
	return redirect(url_for('user', username=username))
@app.route('/explore')
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
		page,app.config['POSTS_PER_PAGE'],
		False
	)
	page=request.args.get(
		'page',
		1,
		type=int
	)
	posts=Post.query.order_by(Post.timestamp.desc()).paginate(
		page,
		app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('explore',page=posts.next_num)if posts.has_next else None
	prev_url=url_for('explore',page=posts.prev_num)if posts.has_prev else None
	return render_template(
		'index.html',
		title='Explore',
		posts=posts.items,
		next_url=next_url,
		prev_url=prev_url
	)
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash(_('Check your email for the instructions to reset your password'))
		return redirect(url_for('login'))
	return render_template(
		'reset_password_request.html',
		title='Reset Password',
		form=form
	)
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash(_('Your password has been reset.'))
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)


@app.route('/trajectories')
@login_required
def trajectories():
	page=request.args.get(
		'page',
		1,
		type=int
	)
	trajectories=Trajectory.query.paginate(
		page,
		10,#app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('trajectories',page=trajectories.next_num)if trajectories.has_next else None
	prev_url=url_for('trajectories',page=trajectories.prev_num)if trajectories.has_prev else None
	return render_template(
		'trajectories.html',
		trajectories=trajectories.items,
		next_url=next_url,
		prev_url=prev_url
	)

@app.route('/cpu', methods=['GET'])
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
		10,#app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('cpu',page=rows.next_num)if rows.has_next else None
	prev_url=url_for('cpu',page=rows.prev_num)if rows.has_prev else None
	return render_template(
		'cpu.html',
		headings=headings,
		rows=rows.items,
		next_url=next_url,
		prev_url=prev_url
	)
@app.route('/cpu', methods=['POST'])
def cpu_post():
	try:
		print(json.dumps(request.get_json(),indent=4))
		c=Cpu(
			ts=parse(request.get_json()['ts']),
			cpu=request.get_json()['cpu']
		)
		db.session.add(c)
		db.session.commit()
	except Exception as E:
		print(E)
	#print(request.get_json()['cpu'])
	return {'msg':'ok'}
@app.route('/psutil', methods=['GET'])
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
@app.route('/tables', methods=['GET'])
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
	for t in db.Model._decl_class_registry.values():
		try:
			table={}
			table['name']=t.__name__
			table['cols']=t.__table__.columns.keys()
			tables.append(table)
		except Exception as E:
			print(str(E))		
	return render_template(
		'tables.html',
		tables=tables
	)
#for o in db.Model._decl_class_registry.values():
#...:     try:
#...:         r=o.query.all()
#...:     except Exception as E:
#...:         print(E)
#...:
#...:
# db.Model._decl_class_registry.get('Post')
#Trajectory.__table__.columns.keys()
@app.route('/table/<tablename>')
@login_required
def show_table(username):
	headings=[]

	for a in db.Model._decl_class_registry.get(tablename).__table__.columns:
		headings.append(a.name)
	page=request.args.get(
		'page',
		1,
		type=int
	)
	rows=db.Model._decl_class_registry.get(tablename).query.order_by(Cpu.ts.desc()).paginate(
		page,
		10,#app.config['POSTS_PER_PAGE'],
		False
	)
	next_url=url_for('table',tablename=tablename,page=rows.next_num)if rows.has_next else None
	prev_url=url_for('table',tablename=tablename,page=rows.prev_num)if rows.has_prev else None
	return render_template(
		'table.html',
		headings=headings,
		rows=rows.items,
		next_url=next_url,
		prev_url=prev_url
	)

