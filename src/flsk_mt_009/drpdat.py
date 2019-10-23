from datetime import\
	datetime,\
	timedelta
import unittest
from app import\
	app,\
	db
from app.models import\
	User,\
	Post
if __name__=='__main__':
	for a in User.query.filter(User.username.like('%testuser%')).all():
		db.session.delete(a)
	for a in Post.query.filter(Post.body.like('%test%')).all():
		db.session.delete(a)
	db.session.commit()
