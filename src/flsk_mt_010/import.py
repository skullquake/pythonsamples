#!/bin/bash
from datetime import\
	datetime,\
	timedelta
from flask_mail import\
	Message
from app.models import\
	Trajectory
from app import\
        create_app,\
	db
from flask import\
	current_app
import sys
if __name__=='__main__':
	"""
	"""
	app=create_app()
	with app.app_context():
		with open("/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/traj/pvotrja.asc") as f:
			arr_traj=[]
			for l in f:
				try:
					YYYY	=int(l[0:5])
					MM	=int(l[6:9])
					DD	=int(l[9:13])
					VENAU	=float(l[13:19])
					SECLAT	=float(l[19:24])
					SECLON	=float(l[24:31])
					sys.stdout.write(f"{YYYY}|{MM}|{DD}|{VENAU}|{SECLAT}|{SECLON}")
					sys.stdout.write(f"\n")
					traj=Trajectory(YYYY=YYYY,MM=MM,DD=DD,VENAU=VENAU,SECLAT=SECLAT,SECLON=SECLON)
					arr_traj.append(traj)
				except Exception as E:
					print(E)
			for traj in arr_traj:
				db.session.add(traj)
				print(traj)
			db.session.commit()
