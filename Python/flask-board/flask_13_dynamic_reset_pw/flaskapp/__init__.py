from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '42dd46dc9a5e66336105b6d43ba0d85b'
# sets the config to use sqlite, with relative path ///, as site.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# creates SQLAlchemy instance, inheriting app
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# login_required section
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' # class='info' is boostrap
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


from flaskapp import routes