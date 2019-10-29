import os
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
	jsonify,\
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
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

import requests
from app.excel import bp
import random
import json
import flask_excel as excel
import xlsxwriter
import math
@bp.route('/home',methods=['GET'])
@login_required
def home():
	return render_template(
		"excel.html"
	)
@bp.route('/test',methods=['GET'])
def test():
	return excel.make_response_from_array([[1, 2], [3, 4]], "xls","a.xls")
@bp.route('/test2',methods=['GET'])
def test2():
	workbook=xlsxwriter.Workbook('hello.xlsx')
	output=BytesIO()
	workbook=xlsxwriter.Workbook(output, {'in_memory': True})
	worksheet=workbook.add_worksheet()

	# Some data we want to write to the worksheet.
	expenses = (
	    ['Rent', 1000],
	    ['Gas',   100],
	    ['Food',  300],
	    ['Gym',    50],
	)

	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0

	# Iterate over the data and write it out row by row.
	for item, cost in (expenses):
	    worksheet.write(row, col,     item)
	    worksheet.write(row, col + 1, cost)
	    row += 1

	# Write a total using a formula.
	worksheet.write(row, 0, 'Total')
	worksheet.write(row, 1, '=SUM(B1:B4)')


	workbook.close()
	output.seek(0)
	ret=send_file(
		output,
		mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
		as_attachment=True,
		conditional=False,
		attachment_filename='asdf.xlsx'
	)
	return ret;
@bp.route('/test3',methods=['GET'])
def test3():
	wnam='hello.xlsx'
	workbook=xlsxwriter.Workbook(wnam)
	output=BytesIO()
	workbook=xlsxwriter.Workbook(output, {'in_memory': True})
	worksheet=workbook.add_worksheet()
	for sidx in range(0,30):
		row=0
		col=0+sidx*2
		dbrs=db.Model._decl_class_registry.get("Vec2F").query.limit(4096).all()
		for dbrow in dbrs:
			worksheet.write(row,col,dbrow.X)
			worksheet.write(row,col+1,math.floor(col*dbrow.Y*(0.5+random.random()*0.5)))
			row+=1
		_row=row
		worksheet.write(row, col+0, 'Tot')
		worksheet.write(row, col+1, f"=SUM({colnum_string(col+2)}1:{colnum_string(col+2)}{_row})")
		row += 1
		worksheet.write(row, col+0, 'Avg')
		worksheet.write(row, col+1, f"=AVERAGE({colnum_string(col+2)}1:{colnum_string(col+2)}{_row})")
		row += 1
		worksheet.write(row, col+0, 'Min')
		worksheet.write(row, col+1, f"=MIN({colnum_string(col+2)}1:{colnum_string(col+2)}{_row})")
		row += 1
		worksheet.write(row, col+0, 'Max')
		worksheet.write(row, col+1, f"=MAX({colnum_string(col+2)}1:{colnum_string(col+2)}{_row})")
		row += 1
		worksheet.write(row, col+0, 'Uniq')
		worksheet.write(row, col+1, f"=SUMPRODUCT(({colnum_string(col+2)}1:{colnum_string(col+2)}{_row}<>\"\")/COUNTIF({colnum_string(col+2)}1:{colnum_string(col+2)}{_row},{colnum_string(col+2)}1:{colnum_string(col+2)}{_row}&\"\"))")
		row += 1

	workbook.close()
	output.seek(0)
	ret=send_file(
		output,
		mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
		as_attachment=True,
		conditional=False,
		attachment_filename=wnam
	)
	return ret;


def colnum_string(n):
	string = ""
	while n > 0:
		n, remainder = divmod(n - 1, 26)
		string = chr(65 + remainder) + string
	return string
