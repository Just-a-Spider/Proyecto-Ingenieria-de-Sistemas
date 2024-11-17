from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username'  , validators=[DataRequired()])
	password = PasswordField('Password'  , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])