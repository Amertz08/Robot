from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user

from forms import LoginForm, SignUpForm
from models import db, User, Account
from ..email import send_email

auth = Blueprint('auth', __name__)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
            and not current_user.verified \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Login Successful', 'success')
        return redirect(url_for('main.index'))  # TODO: Should redirect to dash index
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
        acct = Account(company_name=form.company_name.data)
        db.session.add(acct)
        db.session.commit()
        user = User(acct_id=acct.id,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        token = user.generate_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('You have been registered. A confirmation email is sent to your email address. \
               You have 24 hours to verify your account.')
        db.session.commit()
        login_user(user)
    return render_template('auth/signup.html.j2', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.verified:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have verified your account!')
    elif current_user.confirm(token) == 'expire':
        flash('The confirmation link is expired')
    else:
        flash('The confirmation link is invalid')
        return redirect(url_for('main.404'))
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirm():
    token = current_user.generate_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email is sent to your email address. \
            You have 24 hours to verify your account.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.verified:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html.j2')
