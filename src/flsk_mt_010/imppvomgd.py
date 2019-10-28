#!/bin/bash
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	PvoMgd
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
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1978.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1979.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1980.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1981.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1982.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1983.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1984.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1985.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1986.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1987.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1988.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1989.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1990.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1991.asc",
			"/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer_venus/merged/coho1hr_magplasma_ascii/pvo_1992.asc"
		]
		for p in paths:
			with open(p) as f:
				arr_mag=[]
				for l in f:
					try:
						F1=int(l[0:3])
						F2=int(l[4:8])
						F3=int(l[9:11])
						F4=float(l[12:18])
						F5=float(l[19:25])
						F6=float(l[26:32])
						F7=float(l[33:39])
						F8=float(l[40:46])
						F9=float(l[47:53])
						F10=float(l[54:60])
						F11=float(l[61:67])
						F12=float(l[68:74])
						F13=float(l[75:81])
						F14=float(l[82:88])
						F15=float(l[89:95])
						F16=float(l[96:102])
						F17=float(l[103:109])
						F18=float(l[110:116])
						F19=float(l[117:123])
						F20=float(l[124:132])
						F21=float(l[133:140])
						sys.stdout.write(f"{F1}|{F2}|{F3}|{F4}|{F5}|{F6}|{F7}|{F8}|{F9}|{F10}|{F11}|{F12}|{F13}|{F14}|{F15}|{F16}|{F17}|{F18}|{F19}|{F20}|{F21}")
						sys.stdout.write(f"\n")
						mag=PvoMgd(F1=F1,F2=F2,F3=F3,F4=F4,F5=F5,F6=F6,F7=F7,F8=F8,F9=F9,F10=F10,F11=F11,F12=F12,F13=F13,F14=F14,F15=F15,F16=F16,F17=F17,F18=F18,F19=F19,F20=F20,F21=F21)
						arr_mag.append(mag)
					except Exception as E:
						print(E)
				for mag in arr_mag:
					db.session.add(mag)
					print(mag)
				db.session.commit()
