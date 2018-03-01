from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo

from models import User, Account

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not user.check_password(self.password.data):
            raise ValidationError('Invalid Email/Password')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not user.check_password(self.password.data):
            raise ValidationError('Invalid Email/Password')

class SignUpForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')

    submit = SubmitField('Sign Up')

    def validate_company_name(self, field):
        if Account.query.filter_by(company_name=field.data).first():
            raise ValidationError('Account already exists')

    def validate_email(self, field):
        if Account.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')
