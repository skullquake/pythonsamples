#!/bin/bash
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	Vec2F
from datetime import\
	datetime,\
	timedelta
from app import\
	db
from flask import\
	current_app
import math
import sys
if __name__=='__main__':
	"""
	"""
	app=create_app()
	with app.app_context():
		db.session.query(Vec2F).delete()
		db.session.commit()
		for a in range(8192):
			b=Vec2F(X=a,Y=math.sin(a/100))
			db.session.add(b)
		db.session.commit()
