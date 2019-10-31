from app import\
	db
from datetime import\
	datetime
from werkzeug.security import\
	generate_password_hash,\
	check_password_hash
from flask_login import\
	UserMixin
from flask import\
	current_app
from app import\
	login
from hashlib import\
	md5
import jwt
from time import\
	time
followers=db.Table(
	'followers',
	db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
	db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
)
class User(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),index=True,unique=True)
	email=db.Column(db.String(120),index=True,unique=True)
	password_hash=db.Column(db.String(128))
	about_me=db.Column(db.String(140))
	last_seen=db.Column(db.DateTime,default=datetime.utcnow)
	posts=db.relationship(
		'Post',
		backref='author',
		lazy='dynamic'
	)
	followed=db.relationship(
		'User',
		secondary=followers,
		primaryjoin=(followers.c.follower_id==id),
		secondaryjoin=(followers.c.followed_id==id),
		backref=db.backref('followers',lazy='dynamic'),
		lazy='dynamic'
	)
	def __repr__(self):
		return '<User {}>'.format(self.username)
	def set_password(self,password):
		self.password_hash=generate_password_hash(password)
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)
	def avatar(self,size):
		digest=md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)
	def follow(self,user):
		if not self.is_following(user):
			self.followed.append(user)
	def unfollow(self,user):
		if self.is_following(user):
			self.followed.remove(user)
	def is_following(self,user):
		return self.followed.filter(
			followers.c.followed_id==user.id).count()>0
	def followed_posts(self):
		return Post.query.join(
			followers,(followers.c.followed_id==Post.user_id)
		).filter(
			followers.c.follower_id==self.id
		).order_by(
			Post.timestamp.desc()
		)
	def followed_posts(self):
		followed=Post.query.join(
			followers,
			(
				followers.c.followed_id==Post.user_id
			)
		).filter(
			followers.c.follower_id==self.id
		)
		own=Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.timestamp.desc())
	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
		    {'reset_password': self.id, 'exp': time() + expires_in},
		    current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
	@staticmethod
	def verify_reset_password_token(token):
		try:
			id=jwt.decode(
				token,
				current_app.config['SECRET_KEY'],
				algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)
class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	body=db.Column(db.String(140))
	timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
	def __repr__(self):
		return '<Post {}>'.format(self.body)
class Trajectory(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	YYYY=db.Column(db.Integer)
	MM=db.Column(db.Integer)
	DD=db.Column(db.Integer)
	VENAU=db.Column(db.Float)
	SECLAT=db.Column(db.Float)
	SECLON=db.Column(db.Float)
class Cpu(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	ts=db.Column(db.DateTime,default=datetime.utcnow)
	cpu=db.Column(db.String)
class Test(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	ts=db.Column(db.DateTime,default=datetime.utcnow)
	cpu=db.Column(db.String)
class Mag(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	YY      =db.Column(db.Integer)
	MM      =db.Column(db.Integer)
	DD      =db.Column(db.Integer)
	HH      =db.Column(db.Integer)
	BX_VSO  =db.Column(db.Float)
	BY_VSO  =db.Column(db.Float)
	BZ_VSO  =db.Column(db.Float)
	BT      =db.Column(db.Float)
	VSOX    =db.Column(db.Float)
	VSOY    =db.Column(db.Float)
	VSOZ    =db.Column(db.Float)
class PvoMgd(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	F1=db.Column(db.Integer)
	F2=db.Column(db.Integer)
	F3=db.Column(db.Integer)
	F4=db.Column(db.Float)
	F5=db.Column(db.Float)
	F6=db.Column(db.Float)
	F7=db.Column(db.Float)
	F8=db.Column(db.Float)
	F9=db.Column(db.Float)
	F10=db.Column(db.Float)
	F11=db.Column(db.Float)
	F12=db.Column(db.Float)
	F13=db.Column(db.Float)
	F14=db.Column(db.Float)
	F15=db.Column(db.Float)
	F16=db.Column(db.Float)
	F17=db.Column(db.Float)
	F18=db.Column(db.Float)
	F19=db.Column(db.Float)
	F20=db.Column(db.Float)
	F21=db.Column(db.Float)
class PvoPla(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	F1=db.Column(db.String)
	F2=db.Column(db.Integer)
	F3=db.Column(db.Integer)
	F4=db.Column(db.Integer)
	F5=db.Column(db.Float)
	F6=db.Column(db.Float)
	F7=db.Column(db.Float)
	F8=db.Column(db.Float)
	F9=db.Column(db.Float)
class Pspa(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	F1=db.Column(db.Integer)
	F2=db.Column(db.Integer)
	F3=db.Column(db.Integer)
	F4=db.Column(db.Integer)
	F5=db.Column(db.Integer)
class P10HvmPls(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	F1=db.Column(db.Integer)
	F2=db.Column(db.Integer)
	F3=db.Column(db.Integer)
	F4=db.Column(db.Float)
	F5=db.Column(db.Float)
	F6=db.Column(db.Float)
	F7=db.Column(db.Float)
	F8=db.Column(db.Float)
	F9=db.Column(db.Float)
	F10=db.Column(db.Float)
	F11=db.Column(db.Float)
	F12=db.Column(db.Float)
	F13=db.Column(db.Float)
	F14=db.Column(db.Float)
	F15=db.Column(db.Float)
	F16=db.Column(db.Float)
	F17=db.Column(db.Float)
	F18=db.Column(db.Float)
	F19=db.Column(db.Float)
	F20=db.Column(db.Float)
class P6IMFBRRTN(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	YYYY=db.Column(db.Integer)
	DOY=db.Column(db.Integer)
	HR=db.Column(db.Integer)
	RTN=db.Column(db.Float)
#-------------------------------------------------------------------------------
#HR
#-------------------------------------------------------------------------------
class Department(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	Name=db.Column(db.String)
	employees=db.relationship(
		'Employee',
		backref='department',
		lazy='dynamic'
	)
class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	Name=db.Column(db.String)
	department_id=db.Column(db.Integer,db.ForeignKey('department.id'))
	schedules=db.relationship(
		'Schedule',
		backref='employee',
		lazy='dynamic'
	)
class Schedule(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	t0=db.Column(db.DateTime,default=datetime.utcnow)
	t1=db.Column(db.DateTime,default=datetime.utcnow)
	description=db.Column(db.String)
	employee_id=db.Column(db.Integer,db.ForeignKey('employee.id'))
#todo
class Task(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	description=db.Column(db.String)

#-------------------------------------------------------------------------------
#//HR
#-------------------------------------------------------------------------------
#plotting
#-------------------------------------------------------------------------------
class Dataset(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	vec2s=db.relationship(
		'Vec2F',
		backref='dataset',
		lazy='dynamic'
	)
	vec3s=db.relationship(
		'Vec3F',
		backref='dataset',
		lazy='dynamic'
	)
class Vec2F(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	dataset_id=db.Column(db.Integer,db.ForeignKey('dataset.id'))
	X=db.Column(db.Float)
	Y=db.Column(db.Float)
class Vec3F(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	dataset_id=db.Column(db.Integer,db.ForeignKey('dataset.id'))
	X=db.Column(db.Float)
	Y=db.Column(db.Float)
	Z=db.Column(db.Float)

#-------------------------------------------------------------------------------
#//plotting
#-------------------------------------------------------------------------------
@login.user_loader
def load_user(id):
	return User.query.get(int(id))
