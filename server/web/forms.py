import yaml

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, \
                        HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from models import User, Account, Facility, Layout
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


class AddFacilityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save Facility')

    def validate_name(self, field):
        if Facility.query.filter(
            Facility.name == field.data,
            Facility.acct_id == current_user.acct_id
        ).first():
            raise ValidationError('Facility with that name already exists')

class DeleteFacilityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Delete')

    def validate_name(self, field):
        if not Facility.query.filter(
            Facility.name == field.data,
            Facility.acct_id == current_user.acct_id
        ).first():
            raise ValidationError('Invalid Facility')

class UpdateFacilityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    facility_id = HiddenField('facility_id', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_facility_id(self, field):
        if not Facility.query.filter(
            Facility.id == field.data,
            Facility.acct_id == current_user.acct_id
        ).first():
            raise ValidationError(f'facility_id: {field.data} does not exist')

    def validate_name(self, field):
        if Facility.query.filter(
            Facility.name == field.data,
            Facility.acct_id == current_user.acct_id
        ).first():
            raise ValidationError('Facility with that name already exists')


class AddLayoutForm(FlaskForm):
    facility_id = HiddenField('facility_id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    layout = TextAreaField('Layout', validators=[DataRequired()])
    submit = SubmitField('Create layout')

    def validate_facility_id(self, field):
        if not Facility.query.filter(
            Facility.id == field.data,
            Facility.acct_id == current_user.acct_id
        ).first():
            raise ValidationError(f'facility_id: {field.data} does not exist')

    def validate_name(self, field):
        if Layout.query.filter(
            Layout.facility_id == self.facility_id.data,
            Layout.name == field.data
        ).first():
            raise ValidationError('Layout name already exists')

    def validate_layout(self, field):
        try:
            data = yaml.load(field.data)
            print('Yaml data', data)
            if not isinstance(data, dict):
                raise ValidationError('Invalid YAML')

            if 'nodes' not in data.keys():
                raise ValidationError('"nodes:" missing from layout definition')
            if not isinstance(data['nodes'], list):
                raise ValidationError('nodes: should be a list')

            # Validate each node entry
            for i, node in enumerate(data['nodes']):
                if not isinstance(node, dict):
                    raise ValidationError(f'Value "{n}" in nodes is not a dictionary')
                if 'name' not in node.keys():
                    raise ValidationError(f'"name:" should be a field in node {i}')
                if not isinstance(node['name'], str):
                    raise ValidationError(f'"name:" should be a string in node {i}')
                if 'connections' not in node.keys():
                    raise ValidationError(f'"connections:" should be a field in node {i}')
                if not isinstance(node['connections'], list):
                    raise ValidationError(f'"connections:" should be a list in node {i}')
        except yaml.YAMLError as e:
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                raise ValidationError(f'Parse error line: {mark.line} column: {mark.column + 1}')
            else:
                raise ValidationError('Invalid YAML layout')
