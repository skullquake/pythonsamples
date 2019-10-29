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
from datetime import\
	datetime
from dateutil.parser import\
	parse
from flask_babel import \
	_
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from app.midi import bp
from midiutil import MIDIFile
@bp.route('/midi',methods=['GET','POST'])
@login_required
def midi():
	return render_template(
		"midi.html"
	)
@bp.route('/genmidi',methods=['GET'])
def genmidi():
	print('genmidi')
	degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
	track	= 0
	channel  = 0
	time	 = 0	# In beats
	duration = 1	# In beats
	tempo	= 60   # In BPM
	volume   = 100  # 0-127, as per the MIDI standard
	
	MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
						  # automatically)
	MyMIDI.addTempo(track, time, tempo)
	MyMIDI.addTempo(track, time, tempo)
	
	for i, pitch in enumerate(degrees):
		MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
	with open("major-scale.mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)
	download_filename = "../major-scale.mid"
	return(send_file(filename_or_fp = download_filename,mimetype="audio/midi",as_attachment=True))
