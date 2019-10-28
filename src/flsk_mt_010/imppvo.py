#!/bin/bash
from app import\
        db,\
        create_app,\
        cli
from app.models import\
        User,\
        Post,\
        Trajectory,\
        Cpu
from datetime import\
	datetime,\
	timedelta
from app import\
	db
from flask import\
	current_app
from app.models import\
	Mag
import sys
if __name__=='__main__':
	"""
	"""
	app=create_app()
	with app.app_context():
		with open("/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/mag/hour/pvomag88.asc") as f:
			arr_mag=[]
			for l in f:
				try:
					YY	=int(l[1:3])
					MM	=int(l[4:6])
					DD	=int(l[7:9])
					HH	=int(l[10:12])
					BX_VSO	=float(l[13:22])
					BY_VSO	=float(l[23:32])
					BZ_VSO	=float(l[33:42])
					BT	=float(l[43:52])
					VSOX	=float(l[53:61])
					VSOY	=float(l[62:70])
					VSOZ	=float(l[71:79])
					sys.stdout.write(f"{YY}|{MM}|{DD}|{HH}|{BX_VSO}|{BY_VSO}|{BZ_VSO}|{BT}|{VSOX}|{VSOY}|{VSOZ}")
					sys.stdout.write(f"\n")
					mag=Mag(YY=YY,MM=MM,DD=DD,HH=HH,BX_VSO=BX_VSO,BY_VSO=BY_VSO,BZ_VSO=BZ_VSO,BT=BT,VSOX=VSOX,VSOY=VSOY,VSOZ=VSOZ)
					arr_mag.append(mag)
				except Exception as E:
					print(E)
			for mag in arr_mag:
				db.session.add(mag)
				print(mag)
			db.session.commit()
