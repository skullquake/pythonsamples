#!/bin/bash
import random
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	User
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
		lstusr=[]
		b=User(username=f"ockert",email=f"ockert8080@gmail.com")
		b.set_password('1234!@#$qwerQWER')
		lstusr.append(b)
		for a in lstusr:
			db.session.add(a)
		db.session.commit()
