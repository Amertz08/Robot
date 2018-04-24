import datetime
import enum

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    users = db.relationship('User', backref='account', lazy=True)
    facilites = db.relationship('Facility', backref='account', lazy=True)

    def __init__(self, company_name):
        self.company_name = company_name

    def __repr__(self):
        return f'<Account id: {self.id} company: {self.company_name} >'

    @classmethod
    def get(cls, company_name):
        """
        Returns user model or None with the given email
        """
        return cls.query.filter_by(company_name=company_name).first()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    acct_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))

    verified = db.Column(db.Boolean, default=False)
    verified_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, acct_id, first_name, last_name, email, password):
        self.acct_id = acct_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)

    def __repr__(self):
        return f'<User id: {self.id} first: {self.first_name} last: {self.last_name} >'

    @classmethod
    def get(cls, email):
        """
        Returns user model or None with the given email
        """
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def change_password(self, password):
        self.password = self.set_password(password)

    def generate_token(self, expiration=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.email})

    @classmethod
    def deserialize(cls, token):
        """
        Deserializses token and returns associated user
        @param token : JWT to deserialize
        @return : User model associated with token
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        data = s.loads(token)
        return cls.get(data.get('confirm'))


class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    acct_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    layouts = db.relationship('Layout', backref='facility', lazy=True)

    def __init__(self, acct_id, name):
        self.acct_id = acct_id
        self.name = name


class Layout(db.Model):
    __tablename__ = 'layouts'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    nodes = db.relationship('Node', backref='layout', lazy=True)

class DirectionType(enum.Enum):
    '''Read left to right and thus node_a to node_b'''
    ns = 'north/south'
    ew = 'east/west'

node_connections = db.Table('node_connections',
    db.Column('node_a', db.Integer, db.ForeignKey('nodes.id'), primary_key=True),
    db.Column('node_b', db.Integer, db.ForeignKey('nodes.id'), primary_key=True),
    db.Column('direction', db.Enum(DirectionType), nullable=False)
)

class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    layout_id = db.Column(db.Integer, db.ForeignKey('layouts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    connections = db.relationship('Node',
        secondary=node_connections,
        primaryjoin=node_connections.c.node_a==id,
        secondaryjoin=node_connections.c.node_b==id
    )
