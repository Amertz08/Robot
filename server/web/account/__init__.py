import datetime
from flask import Blueprint, url_for, flash, render_template, redirect, request, abort
from forms import AddUserForm, RemoveUserForm, SetPassword
from models import db, User, Account
from utils import send_email, print_debug, log_message
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import SignatureExpired, BadSignature

acct = Blueprint('acct', __name__)

@acct.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(acct_id=current_user.acct_id,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password='pass')
        db.session.add(user)
        db.session.commit()
        token = user.generate_token()

        print_debug(url_for('acct.set_pw', token=token, _external=True))

        send_email(user.email, 'Confirm Your Account', 'set-pw', 'info@example.com', user=user, token=token)

        flash('New user has been added. A confirmation email is sent to user\'s email address. \
                The link will expire after 24 hours.')
        log_message(f'acct_id: {current_user.acct_id}, {user.first_name} has been added')
        return redirect(url_for('dash.index'))
    return render_template('account/add-user.html.j2', form=form)


@acct.route('/remove-user', methods=['GET', 'POST'])
@login_required
def rm_user():
    form = RemoveUserForm()
    if form.validate_on_submit():
        acct = Account.get(form.company_name.data)
        if acct:
            user = User.get(form.email.data)
            if user:
                db.session.delete(user)
                db.session.commit()
                log_message(f'acct_id: {acct.id},\t user: {user.first_name} has been removed')
                flash('User has been removed')
                if user == current_user:
                    logout_user()
            else:
                flash('User doesn\'t exist')
        else:
            flash('Invalid company name')
        return redirect(url_for('dash.index'))
    return render_template('account/rm-user.html.j2', form=form)


@acct.route('/set-pw', methods=['GET', 'POST'])
def set_pw():
    token = request.args.get('token')
    if not token:
        log_message('no token attempted verification')
        abort(404)

    try:
        user = User.deserialize(token)
    except SignatureExpired:
        flash('The link has expired')
        log_message('expired token on account verification')
        return redirect(url_for('dash.index'))
    except BadSignature:
        flash('Invalid token', 'danger')
        log_message('bad signature verification attempt')
        return redirect(url_for('main.index'))

    form = SetPassword()
    user.verified = True
    user.verified_date = datetime.datetime.utcnow()
    log_message(f'user_id: {user.id} verified their account')

    if form.validate_on_submit():
        log_message(f'user_id: {user.id} set password')
        user.change_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password set', 'success')
        login_user(user)
        return redirect(url_for('dash.index'))
    return render_template('account/set-pw.html.j2', form=form)
