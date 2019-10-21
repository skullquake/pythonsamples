from app import app,db
from app.models import User,Post
@app.shell_context_processor
def make_shell_context():
	"""
	The following function in microblog.py creates a shell context that adds the database instance and models to the shell session:
	"""
	return {'db': db, 'User': User, 'Post': Post}

