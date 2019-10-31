#!/bin/bash
import random
from app import\
        db,\
        create_app,\
        cli
from app.models import\
	Department,\
	Employee,\
	Schedule
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
	ndep=4
	nemp=8
	nsch=8
	tasks=['task0','task1','task3']
	with app.app_context():
		db.session.query(Department).delete()
		db.session.query(Employee).delete()
		db.session.query(Schedule).delete()
		dateNow=datetime.today()
		for a in range(ndep):
			print(f"Generating department {a}")
			dep=Department(
				Name=f"Department {a}"
			)
			db.session.add(dep)
			for b in range(a*nemp,a*nemp+nemp):
				emp=Employee(
					Name=f"Employee {b}",
					department=dep
				)
				db.session.add(emp)
				for c in range(nsch):
					for d in range(8):
						sch=Schedule(
							description=random.choice(tasks),
							t0=datetime(
								dateNow.year,
								dateNow.month,
								c+1,
								d,
								0,
								0,
								0
							),
							t1=datetime(
								dateNow.year,
								dateNow.month,
								c+1,
								d,
								59-random.randint(0,30),
								0,
								0
							),
							employee=emp
						)
						trand=random.randint(0,8)
						db.session.add(sch)
			db.session.commit()
