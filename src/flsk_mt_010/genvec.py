#!/bin/bash
import random
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	Vec2F,\
	Vec3F,\
	Dataset
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
		_xmin=0
		_xmax=1024
		_ymin=0
		_ymax=640
		_zmin=0
		_zmax=1
		nset=1
		nvec=4096
		db.session.query(Dataset).delete()
		db.session.query(Vec2F).delete()
		db.session.query(Vec3F).delete()
		db.session.commit()
		for a in range(nset):
			print(f"Generating dataset {a}")
			dset=Dataset()
			db.session.add(dset)
#			for b in range(nvec):
#				vx=random.random()
#				vx*=vx
#				vx*=(abs(_xmin-_xmax))+_xmin
#				vy=random.random()
#				vy*=vy
#				vy*=(abs(_ymin-_ymax))+_ymin
#				vec=Vec2F(
#					dataset=dset,
#					X=vx,
#					Y=vy
#				)
#				db.session.add(vec)
			for b in range(nvec):
				vx=random.random()
				vx*=vx
				vx*=vx
				vx=b/nvec
				vx*=(abs(_xmin-_xmax))+_xmin
				vy=random.random()
				vy*=vy
				vy*=vy
				#vy=1-vy
				vy*=(abs(_ymin-_ymax))+_ymin
				vz=random.random()
				vec=Vec3F(
					dataset=dset,
					X=vx,
					Y=vy,
					Z=vz
				)
				db.session.add(vec)

			db.session.commit()
