from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from models import User, Account
from utils import log_message

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not user.check_password(self.password.data):
            log_message(f'{self.email.data} invalid login attempt')
            raise ValidationError('Invalid Email/Password')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not user.check_password(self.password.data):
            log_message(f'{self.email.data} invalid login attempt')
            raise ValidationError('Invalid Email/Password')


class SignUpForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=64)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')

    submit = SubmitField('Sign Up')

    def validate_company_name(self, field):
        if Account.query.filter_by(company_name=field.data).first():
            raise ValidationError('Account already exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

class SendResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Update')


class AddUserForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=64)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')

    submit = SubmitField('Add')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

    def validate_company(self, field):
        if Account.query.filter_by(company_name=field.data) == None :
            raise ValidationError('Company doesn\'t exist')


class RemoveUserForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Remove')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data) == None:
            raise ValidationError('User doesn\'t exist')
