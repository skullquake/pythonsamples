#!/bin/bash
import random
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
		_min=-8
		_max=8
		db.session.query(Vec2F).delete()
		db.session.commit()
		for a in range(128):
			#b=Vec2F(X=a,Y=math.sin(a/100))
			b=Vec2F(
				X=random.random()*(abs(_min-_max))+_min,
				Y=random.random()*(abs(_min-_max))+_min
			)
			db.session.add(b)
		db.session.commit()
