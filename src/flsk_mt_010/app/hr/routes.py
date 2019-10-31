import io
from io import\
	StringIO,\
	BytesIO
import flask
from flask import\
	render_template,\
	flash,\
	redirect,\
	url_for,\
	request,\
	current_app,\
	send_file
from flask_login import\
	current_user,\
	login_user,\
	logout_user,\
	login_required
from werkzeug.urls import\
	url_parse
from app import \
	db
from dateutil.parser import\
	parse
from flask_babel import \
	_
from sqlalchemy import\
	create_engine,\
	func
from sqlalchemy import MetaData
from sqlalchemy import Table
from app.models import\
	Department,\
	Employee,\
	Schedule
import requests
from app.hr import bp
@bp.route('/home',methods=['GET'])
@login_required
def home():
	departments=Department.query.all()
	#rowcount=db.Model._decl_class_registry.get(tablename).query.count()
	#for a in Department.query.all():
	#	for b in a.employees.all():
	#		for c in b.schedules.all():
	#			print(f"{a.Name},{b.Name},{c.description}")
	return render_template(
		"hr/home.html",
		departments=departments
	)
@bp.route('/show_department/<id>',methods=['GET'])
@login_required
def show_department(id):
	department=Department.query.filter_by(id=id).first()
	employees={
		"headings":[],
		"rows":[]
	}
	for a in Employee.__table__.columns:
		employees["headings"].append(a.name)
	employees["rows"]=department.employees.all()
	return render_template(
		"hr/department.html",
		department=department,
		employees=employees
	)
@bp.route('/show_employee/<id>',methods=['GET'])
@login_required
def show_employee(id):
	employee=Employee.query.filter_by(id=id).first()
	schedules={
		"headings":[],
		"rows":[]
	}
	for a in Schedule.__table__.columns:
		schedules["headings"].append(a.name)
	schedules["rows"]=employee.schedules.all()
	dates=[]
	for s in schedules["rows"]:
		dates.append({'dsc':s.description,'t0':s.t0,'t1':s.t1})
	return render_template(
		"hr/employee.html",
		employee=employee,
		schedules=schedules,
		dates=dates
	)

