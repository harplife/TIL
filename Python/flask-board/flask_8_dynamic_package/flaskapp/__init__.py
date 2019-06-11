from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '42dd46dc9a5e66336105b6d43ba0d85b'
# sets the config to use sqlite, with relative path ///, as site.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# creates SQLAlchemy instance, inheriting app
db = SQLAlchemy(app)

from flaskapp import routes