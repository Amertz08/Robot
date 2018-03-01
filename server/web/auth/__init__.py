from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user

from forms import LoginForm, SignUpForm
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Login Successful', 'success')
        return redirect(url_for('main.index')) # TODO: Should redirect to dash index
    return render_template('auth/login.html.j2', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        pass
    return render_template('auth/signup.html.j2', form=form)


