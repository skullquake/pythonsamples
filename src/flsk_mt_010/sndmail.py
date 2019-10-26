#!/bin/bash
from datetime import\
	datetime,\
	timedelta
from app import\
	app,\
	mail
from flask_mail import\
	Message
if __name__=='__main__':
	with app.app_context():
		for a in range(4096*8):
			try:
				print(f"sending")
				msg=Message(
					'test subject',
					sender=app.config['ADMINS'][0],
					recipients=['ockert8080@gmail.com']
				)
				msg.body='text body'
				msg.html='<h1>HTML body</h1>'
				mail.send(msg)
				print(f"done")
			except Exception as E:
				print(f"{E}")
