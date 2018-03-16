import datetime

from flask import Blueprint, abort, render_template, flash, \
                    request, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from forms import LoginForm, SignUpForm, SendResetForm, ResetPasswordForm
from models import db, User, Account
from utils import send_email, print_debug

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.email.data)
        login_user(user)
        if not user.verified:
            url = url_for('auth.resend_confirm')
            link = f'<a href="{url}">Resend</a>'
            flash(f'Your account is still not verified. {link}', 'danger')
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
        db.session.commit()
        token = user.generate_token()
        print_debug(url_for('auth.confirm', token=token, _external=True))
        send_email(user.email, 'Confirm Your Account',
                   'confirm', 'info@example.com', user=user, token=token)
        flash('You have been registered. A confirmation email is sent to your email address. \
               You have 24 hours to verify your account.')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html.j2', form=form)


@auth.route('/send-reset', methods=['GET', 'POST'])
def send_reset():
    form = SendResetForm()
    if form.validate_on_submit():
        user = User.get(form.email.data)
        if user:
            token = user.generate_token()
            print_debug(url_for('auth.reset', token=token, _external=True))
            send_email(user.email, 'Reset your password',
                    'reset-pw', 'info@example.com',token=token
            )
        else:
            print('User not found') # TODO: actually log invalid reset attemps
        flash('An email will be sent with a link to reset your password', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/send-reset.html.j2', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    token = request.args.get('token')
    if not token:
        abort(404)

    try:
        user = User.deserialize(token)
    except SignatureExpired:
        flash('Expired Token', 'danger')
        return redirect(url_for('main.index'))
    except BadSignature:
        flash('Invalid token', 'danger') # TODO: log invalid token attempt w/ IP
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.change_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password reset', 'success')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/reset.html.j2', form=form)


@auth.route('/confirm')
def confirm():
    token = request.args.get('token')
    if not token:
        abort(404) # TODO: log
    try:
        user = User.deserialize(token)
        if user.verified:
            flash('Your account is already verified')
            return redirect(url_for('main.index'))
        user.verified = True
        user.verified_date = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash('You have verified your account!') # TODO: log
        return redirect(url_for('main.index'))
    except SignatureExpired: # TODO: log
        flash('The confirmation link is expired')
    except BadSignature:
        abort(404) # TODO: log
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
    return redirect(url_for('main.index'))
