#!/bin/bash
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	P10HvmPls
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
		pfx="/home/skullquake/dat/nasa/spdf.sci.gsfc.nasa.gov/pub/data/pioneer/pioneer10/merged/coho1hr_magplasma_ascii/"
		paths=[
			pfx+"p10_1972.asc",
			pfx+"p10_1973.asc",
			pfx+"p10_1974.asc",
			pfx+"p10_1975.asc",
			pfx+"p10_1976.asc",
			pfx+"p10_1977.asc",
			pfx+"p10_1978.asc",
			pfx+"p10_1979.asc",
			pfx+"p10_1980.asc",
			pfx+"p10_1981.asc",
			pfx+"p10_1982.asc",
			pfx+"p10_1983.asc",
			pfx+"p10_1984.asc",
			pfx+"p10_1985.asc",
			pfx+"p10_1986.asc",
			pfx+"p10_1987.asc",
			pfx+"p10_1988.asc",
			pfx+"p10_1989.asc",
			pfx+"p10_1990.asc",
			pfx+"p10_1991.asc",
			pfx+"p10_1992.asc",
			pfx+"p10_1993.asc",
			pfx+"p10_1994.asc",
			pfx+"p10_1995.asc"
		]
		for p in paths:
			with open(p) as f:
				sys.stdout.write(f"Importing {p}...")
				arr_p10hvmpls=[]
				for l in f:
					try:
						F1=int(l[0:4])
						F2=int(l[5:8])
						F3=int(l[9:11])
						F4=float(l[12:18])
						F5=float(l[19:25])
						F6=float(l[26:32])
						F7=float(l[33:41])
						F8=float(l[42:50])
						F9=float(l[51:59])
						F10=float(l[60:68])
						F11=float(l[69:75])
						F12=float(l[76:82])
						F13=float(l[83:89])
						F14=float(l[90:98])
						F15=float(l[90:98])
						F16=float(l[99:106])
						F17=float(l[108:120])
						F18=float(l[108:120])
						F19=float(l[121:133])
						F20=float(l[134:146])
						pspa=P10HvmPls(F1=F1,F2=F2,F3=F3,F4=F4,F5=F5,F6=F6,F7=F7,F8=F8,F9=F9,F10=F10,F11=F11,F12=F12,F13=F13,F14=F14,F15=F15,F16=F16,F17=F17,F18=F18,F19=F19,F20=F20)
						arr_p10hvmpls.append(pspa)
					except Exception as E:
						print(E)
				for pspa in arr_p10hvmpls:
					db.session.add(pspa)
				sys.stdout.write("done\n");
				db.session.commit()
