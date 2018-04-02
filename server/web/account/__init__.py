from flask import Blueprint, url_for, flash, render_template, redirect
from forms import AddUserForm
from models import db, User, Account
from utils import send_email, print_debug, log_message
from flask_login import login_user, login_required

acct = Blueprint('acct', __name__)

@acct.route('/add-user')
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        acct = Account(company_name=form.company_name.data)
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
        log_message(f'acct_id: {acct.id} just signed up') #TODO: maybe not acct.id?
        return redirect(url_for('main.index'))
    return render_template('account/add-user.html.j2', form=form)
