from app import\
	db,\
	create_app,\
	cli
from app.models import\
	User,\
	Post,\
	Trajectory,\
	Cpu,\
	PvoMgd,\
	Department,\
	Employee,\
	Schedule
app=create_app()
cli.register(app)
@app.shell_context_processor
def make_shell_context():
	"""
	"""
	return {\
		'db':db,\
		'User':User,\
		'Post': Post,\
		'Trajectory':Trajectory,\
		'Cpu':Cpu,\
		'PvoMgd':PvoMgd,\
		'Department':Department,\
		'Schedule':Employee,\
		'Employee':Schedule
	}

