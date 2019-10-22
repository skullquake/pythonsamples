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
	lstusr=[]
	lstpst=[]
	nusr=128
	npst=128
	for a in range(nusr):
		b=User(username=f"testuser{a}",email=f"testuser{a}@test.com")
		b.set_password('1234')
		for c in range(npst):
			d=Post(body=f"test {c}",author=b)
			lstpst.append(d)
		lstusr.append(b)
	for a in lstusr:
		db.session.add(a)
	for a in lstpst:
		db.session.add(a)
	for a in lstusr:
		for b in lstusr:
			a.follow(b)
	db.session.commit()
