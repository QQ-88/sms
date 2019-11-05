from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from sms_agenda.models import User
import phonenumbers


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please change it')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please change it')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SMSForm(FlaskForm):
    phone = StringField('Phone')
    timezone = SelectField(u'Choose your timezone', choices=[('-8', 'UTC-8'), ('-7', 'UTC-7'), ('-6', 'UTC-6'), ('-5', 'UTC-5'),
                            ('-4', 'UTC-4'), ('-3', 'UTC-3'), ('-2', 'UTC-2'), ('-1', 'UTC-1'),
                            ('0', 'UTC'), ('1', 'UTC+1'), ('2', 'UTC+2'), ('3', 'UTC+3'), ('4', 'UTC+4'),
                            ('5', 'UTC+5'), ('6', 'UTC+6'), ('7', 'UTC+7'), ('8', 'UTC+8'),
                            ('9', 'UTC+9'), ('10', 'UTC+10'), ('11', 'UTC+11'), ('12', 'UTC+12')], validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def validate_phone(form, field):
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

        if field.data != current_user.phone:
            user = User.query.filter_by(phone=field.data).first()
            if user:
                raise ValidationError('That phone is taken, please change it')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please change it')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please change it')

    def validate_phone(form, field):
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

        if field.data != current_user.phone:
            user = User.query.filter_by(phone=field.data).first()
            if user:
                raise ValidationError('That phone is taken, please change it')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with this email. Please register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')