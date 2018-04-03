from flask import Blueprint, url_for, flash, render_template, redirect
from forms import AddUserForm, RemoveUserForm
from models import db, User, Account
from utils import send_email, print_debug, log_message
from flask_login import login_user, logout_user, login_required, current_user

acct = Blueprint('acct', __name__)

@acct.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        acct = Account.get(form.company_name.data)
        if acct:
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
            flash('New user have been added. A confirmation email is sent to your email address. \
                       You have 24 hours to verify your account.')
            login_user(user)
            log_message(f'acct_id: {acct.id} just signed up') #TODO: maybe not acct.id?
        else:
            flash('Invalid company name')
        return redirect(url_for('main.index'))
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
        return redirect(url_for('main.index'))
    render_template('account/rm-user.html.j2', form=form)