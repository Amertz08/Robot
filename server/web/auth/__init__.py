import datetime

from flask import Blueprint, abort, render_template, flash, \
                    request, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from forms import LoginForm, SignUpForm, SendResetForm, ResetPasswordForm
from models import db, User, Account
from utils import send_email, print_debug, log_message

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.email.data)
        login_user(user)
        log_message(f'user_id: {user.id} logged in')
        if not user.verified:
            url = url_for('auth.resend_confirm')
            link = f'<a href="{url}">Resend</a>'
            flash(f'Your account is still not verified. {link}', 'danger')
        flash('Login Successful', 'success')
        return redirect(url_for('dash.index'))
    return render_template('auth/login.html.j2', form=form)


@auth.route('/logout')
@login_required
def logout():
    log_message(f'user_id: {current_user.id} logged out')
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
        db.session.commit()
        token = user.generate_token()
        print_debug(url_for('auth.confirm', token=token, _external=True))
        log_message(f'acct_id: {acct.id} just signed up')
        send_email(user.email, 'Confirm Your Account',
                   'confirm', 'info@example.com', user=user, token=token)
        flash('You have been registered. A confirmation email is sent to your email address. \
               You have 24 hours to verify your account.')
        login_user(user)
        return redirect(url_for('dash.index'))
    return render_template('auth/signup.html.j2', form=form)


@auth.route('/send-reset', methods=['GET', 'POST'])
def send_reset():
    form = SendResetForm()
    if form.validate_on_submit():
        log_message(f'{form.email.data} attempted to send password reset email')
        user = User.get(form.email.data)
        if user:
            token = user.generate_token()
            print_debug(url_for('auth.reset', token=token, _external=True))
            send_email(user.email, 'Reset your password',
                    'reset-pw', 'info@example.com',token=token
            )
            log_message(f'user_id: {user.id} sent password reset')
        else:
            log_message(f'{form.email.data} is an invalid email')
        flash('An email will be sent with a link to reset your password', 'success')
        return redirect(url_for('dash.index'))
    return render_template('auth/send-reset.html.j2', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    token = request.args.get('token')
    if not token:
        log_message(f'no token attempted reset')
        abort(404)

    try:
        user = User.deserialize(token)
    except SignatureExpired:
        flash('Expired Token', 'danger')
        log_message('expired token reset attempt')
        return redirect(url_for('main.index'))
    except BadSignature:
        flash('Invalid token', 'danger')
        log_message('bad signature reset attempt')
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        log_message(f'user_id: {user.id} changed password')
        user.change_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password reset', 'success')
        login_user(user)
        return redirect(url_for('dash.index'))
    return render_template('auth/reset.html.j2', form=form)


@auth.route('/confirm')
def confirm():
    token = request.args.get('token')
    if not token:
        log_message('no token attempted verification')
        abort(404)
    try:
        user = User.deserialize(token)
        if user.verified:
            flash('Your account is already verified')
            return redirect(url_for('dash.index'))
        user.verified = True
        user.verified_date = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash('You have verified your account!')
        log_message(f'user_id: {user.id} verified their account')
        return redirect(url_for('dash.index'))
    except SignatureExpired:
        flash('The confirmation link is expired')
        log_message('expired token on account verification')
    except BadSignature:
        log_message('bad signature verification attempt')
        abort(404)
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirm():
    token = current_user.generate_token()
    print_debug(url_for('auth.confirm', token=token, _external=True))
    send_email(current_user.email, 'Confirm Your Account',
               'confirm', 'info@example.com', user=current_user, token=token)
    flash('A new confirmation email is sent to your email address. \
            You have 24 hours to verify your account.')
    log_message(f'user_id: {current_user.id} resent their confirmation email')
    return redirect(url_for('main.index'))
