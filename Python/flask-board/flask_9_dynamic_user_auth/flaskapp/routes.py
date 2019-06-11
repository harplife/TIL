from flask import render_template, url_for, flash, redirect, request
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp.models import User, Post
from flaskapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


posts = [
	{
		'author': 'Ben Kim',
		'title': 'Blog Post 1',
		'content': 'First post content',
		'date_posted': 'April 20, 2018'
	},
	{
		'author': 'Luke Kim',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date_posted': 'April 21, 2018'
	}
]


@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	# this is POST method
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		# python 터미널에서 미리 db.create_all() 해줘야된다.
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		# checks if user email exists,
		user = User.query.filter_by(email=form.email.data).first()
		# and if user input password matches with hasehd password in db
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# if matches, then login_user logs in the user
			login_user(user, remember=form.remember.data)
			# if there is ?next= parameter exists;
			next_page = request.args.get('next')
			# below is awesome python thing
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')