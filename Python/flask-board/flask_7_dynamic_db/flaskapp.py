from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '42dd46dc9a5e66336105b6d43ba0d85b'
# sets the config to use sqlite, with relative path ///, as site.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# creates SQLAlchemy instance, inheriting app
db = SQLAlchemy(app)


# creates User class/model
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	# create relationship
	posts = db.relationship('Post', backref='author', lazy=True)

	# dunder method, magic method
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# creates Post class/mode
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	# setting foreign key using User model id
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"


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
	form = RegistrationForm()
	# this is POST method
	if form.validate_on_submit():
		# f-string lets you pass variables (python 3.6 and above)
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# fake user validation
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check yourname and password.', 'danger')
	return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
	app.run(debug=True)