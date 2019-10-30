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
	ndep=32
	nemp=128
	nsch=16
	with app.app_context():
		db.session.query(Department).delete()
		db.session.query(Employee).delete()
		db.session.query(Schedule).delete()
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
					sch=Schedule(
						description=f"Schedule {c}",
						employee=emp
					)
					db.session.add(sch)
			db.session.commit()
