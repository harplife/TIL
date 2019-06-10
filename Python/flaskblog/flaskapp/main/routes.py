from flask import render_template, Blueprint, flash
from flaskapp.main.forms import LoginForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	return render_template('home.html')


@main.route("/about")
def about():
	greet = "Hello, World!"
	return render_template('about.html', greet=greet)


@main.route("/greet/<string:name>")
def greet(name):
	if name:
		flash(f'Welcome, {name}!', 'success')
	# return render_template('greet.html', name=name)
	return render_template('greet.html')


@main.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# fake user validation
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			return "LOGIN SUCCESS!"
		else:
			return "LOGIN FAILURE"
	return render_template('login.html', title='Login', form=form)