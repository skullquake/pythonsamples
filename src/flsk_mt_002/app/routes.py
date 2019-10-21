from flask import render_template
from app import app
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
	user={'username': 'Miguel'}
	posts=[]
	for a in range(0,10):
		posts.append(
			{
				'author':{'username':f'author {a}'},
				'body':f'post {a}'
			}
		)
	return render_template(
		'index.html',
		title='Home',
		user=user,
		posts=posts
	)
@app.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html',title='Sign In',form=form)

