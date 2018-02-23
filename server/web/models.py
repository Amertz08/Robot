from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(64), unique=True)
    createDate = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    def __repr__(self):
        return '<Account %r>' % self.companyName

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    acct_id = db.Column(db.String(64)) #still need set this to be foreign key
    firstName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))


    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

