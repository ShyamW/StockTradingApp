from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    ssn = IntegerField('ssn', validators=[DataRequired()])
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