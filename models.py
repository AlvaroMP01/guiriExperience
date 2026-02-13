from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import pymysql
from datetime import datetime

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/guiriexperience'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def get_username(self):
        return self.username
    
    def get_role(self):
        return self.role

