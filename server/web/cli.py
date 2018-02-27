import os

import click
from flask.cli import FlaskGroup

from factory import create_app
from models import db, User, Account

def create_wrapper(info):
    return create_app(os.getenv('FLASK_CONFIG') or 'default')

@click.group(cls=FlaskGroup, create_app=create_wrapper)
def cli():
    pass

@cli.command(help='Create db tables')
def createdb():
    db.create_all()

@cli.command(help='Drops and recreates db tables')
def resetdb():
    if click.confirm('This will drop all tables are you sure'):
        db.drop_all()
        db.create_all()

@cli.command(name='testuser', help='Create test user')
def test_user():
    acct = Account(company_name='Test Company')
    db.session.add(acct)
    db.session.commit()
    user = User(
        acct_id=acct.id,
        first_name='Steve',
        last_name='McQueen',
        email='steve@example.com',
        password='pass'
    )
    db.session.add(user)
    db.session.commit()
    click.echo('User Created')



if __name__ == '__main__':
    cli()
