import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, company_name):
        self.company_name = company_name

    def __repr__(self):
        return '<Account %r>' % self.company_name



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    acct_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))

    def __init__(self, acct_id, first_name, last_name, email, password):
        self.acct_id = acct_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)

    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
