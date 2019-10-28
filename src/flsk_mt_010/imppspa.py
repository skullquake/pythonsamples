#!/bin/bash
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	Pspa
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
		paths=[
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus_bus/bims/850-140_km_data/PSPA-00129_DD057809_09-DEC-78.dir/DD057809_F1.ASC"
		]
		for p in paths:
			with open(p) as f:
				sys.stdout.write(f"Importing {p}...")
				arr_pspa=[]
				for l in f:
					try:
						F1=str(l[0:5])
						F2=str(l[6:14])
						F3=str(l[15:21])
						F4=str(l[22:31])
						F5=str(l[32:34])
						#sys.stdout.write(f"{F1}|{F2}|{F3}|{F4}|{F5}|{F6}|{F7}|{F8}|{F9}|")
						#sys.stdout.write(f"\n")
						pspa=Pspa(F1=F1,F2=F2,F3=F3,F4=F4,F5=F5)
						arr_pspa.append(pspa)
					except Exception as E:
						print(E)
				for pspa in arr_pspa:
					db.session.add(pspa)
				sys.stdout.write("done\n");
				db.session.commit()
