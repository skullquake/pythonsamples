from app import\
	app,db
from app.models import\
	User,\
	Post,\
	Trajectory,\
	Cpu
from app import cli
@app.shell_context_processor
def make_shell_context():
	"""
	register ctx
	"""
	return {
		'db':db,
		'User':User,
		'Post': Post,
		'Trajectory':Trajectory,
		'Cpu':Cpu
	}
