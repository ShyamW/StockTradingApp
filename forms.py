from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError
import re


def checkssn(form, field):
    if len(field.data) != 9:
        raise ValidationError('SSN must be 9 digits')
    if not field.data.isdigit():
        raise ValidationError('SSN must only be digits')


def checkphone(form, field):
    if len(field.data) != 10:
        raise ValidationError('Phone number must be 10 digits')
    if not field.data.isdigit():
        raise ValidationError('Phone number must be digits')


def check_password(form, field):
    pattern = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    if not pattern.match(field.data):
        raise ValidationError('Contain at least 1 digit and number and be 8 chars')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), check_password])
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    phonenumber = StringField('phonenumber', validators=[DataRequired(), checkphone])
    ssn = StringField('ssn', validators=[DataRequired(), checkssn])
    submit = SubmitField('Sign In')

    def __repr__(self):
        return str((self.email.data, self.firstname.data, self.lastname.data, self.password.data, self.ssn.data))


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    token = IntegerField('token', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def __repr__(self):
        return str((self.email.data, self.password.data))
