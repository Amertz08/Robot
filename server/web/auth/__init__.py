from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required

from forms import LoginForm
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Login Successful', 'success')
        return redirect(url_for('main.index')) # TODO: fix redirect location
    return render_template('auth/login.html.j2', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('main.index'))
