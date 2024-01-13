# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # Import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session security
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # Initialize LoginManager

from app.models import User
from app import routes
