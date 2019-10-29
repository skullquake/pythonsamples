#!/bin/bash
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	P6IMFBRRTN
from datetime import\
	datetime,\
	timedelta
from app import\
	db
from flask import\
	current_app
import sys
if __name__=='__main__':
	"""
	"""
	app=create_app()
	with app.app_context():
		pfx="/home/skullquake/dat/nasa/pioneer/p6/"
		paths=[
			pfx+"p6IMFBRRTN.txt",
		]
		for p in paths:
			with open(p) as f:
				sys.stdout.write(f"Importing {p}...")
				next(f)
				next(f)
				next(f)
				tbl=[]
				for l in f:
					try:
						YYYY=int(l[0:4])
						DOY=int(l[5:8])
						HR=int(l[9:11])
						RTN=float(l[12:18])
						print(f"{YYYY}|{DOY}|{HR}|{RTN}")
						row=P6IMFBRRTN(YYYY=YYYY,DOY=DOY,HR=HR,RTN=RTN)
						tbl.append(row)
					except Exception as E:
						print(E)
				for row in tbl:
					db.session.add(row)
				sys.stdout.write("done\n");
				db.session.commit()
