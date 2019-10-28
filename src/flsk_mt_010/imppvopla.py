#!/bin/bash
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	PvoPla
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
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/plasma/hour/pvo_78_79h.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/plasma/hour/pvo_80_81h.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/plasma/hour/pvo_82_83h.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/plasma/hour/pvo_84_85h.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/plasma/hour/pvo_86_87h.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/plasma/hour/pvo_88_89h.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/plasma/hour/pvo_90_92h.asc"
		]
		for p in paths:
			with open(p) as f:
				sys.stdout.write(f"Importing {p}...")
				arr_pvopla=[]
				next(f)
				next(f)
				next(f)
				next(f)
				next(f)
				next(f)
				for l in f:
					try:
						F1=str(l[0:4])
						F2=str(l[5:10])
						F3=str(l[11:15])
						F4=str(l[16:20])
						F5=str(l[21:30])
						F6=str(l[31:40])
						F7=str(l[41:50])
						F8=str(l[51:60])
						F9=str(l[61:70])
						#sys.stdout.write(f"{F1}|{F2}|{F3}|{F4}|{F5}|{F6}|{F7}|{F8}|{F9}|")
						#sys.stdout.write(f"\n")
						pvopla=PvoPla(F1=F1,F2=F2,F3=F3,F4=F4,F5=F5,F6=F6,F7=F7,F8=F8,F9=F9)
						arr_pvopla.append(pvopla)
					except Exception as E:
						print(E)
				for pvopla in arr_pvopla:
					db.session.add(pvopla)
					#print(pvopla)
				sys.stdout.write("done\n");
				db.session.commit()
