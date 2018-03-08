import warnings

from flask import Blueprint, abort, render_template, flash, redirect, url_for, current_app, request
from flask_login import login_user, login_required, logout_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from forms import LoginForm, SignUpForm, SendResetForm, ResetPasswordForm
from models import db, User, Account

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
        flash('You have been registered')
        login_user(user)
        return redirect(url_for('main.index'))  # TODO: Should redirect to dash index
    return render_template('auth/signup.html.j2', form=form)

@auth.route('/send-reset', methods=['GET', 'POST'])
def send_reset():
    form = SendResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_token()
            if current_app.config['DEBUG']:
                print(url_for('auth.reset', token=token, _external=True))
        warnings.warn('send_reset not fully implemented')

        flash('An email will be sent with a link to reset your password', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/send-reset.html.j2', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    token = request.args.get('token')
    if not token:
        abort(404)

    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        flash('Expired Token', 'error')
        return redirect(url_for('main.index'))
    except BadSignature:
        flash('Invalid token', 'error') # TODO: log invalid token attempt w/ IP
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id=data.get('confirm')).first()

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.reset_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password reset', 'success')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/reset.html.j2', form=form)
