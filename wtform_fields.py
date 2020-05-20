from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import Users


def invalid_credentials(form, field):
	#username and password checker
	username_entered = form.username.data
	password_entered = field.data

	#Check if credentials is valid
	user_object = Users.query.filter_by(username=username_entered).first()
	if user_object is None:
		raise ValidationError("Username or Password is incorrect")
	elif not pbkdf2_sha256.verify(password_entered, user_object.password):
		raise ValidationError("Username or Password is incorrect")


class RegistrationForm(FlaskForm):
	#Registration form

	username = StringField('username_label', validators=[InputRequired("Username reuired"),
		Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
	password = PasswordField('password_label', validators=[InputRequired("Password reuired"),
		Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
	confirmation_password = PasswordField('confirmation_password_label', validators=[InputRequired("Password reuired"),
		EqualTo('password', message="Passwords must match")])
	submit_button = SubmitField('Create')


	#Check if username exist
	def validate_username(self, username):
		user_object = Users.query.filter_by(username=username.data).first()
		if user_object:
			raise ValidationError("Username already exist")

class LoginForm(FlaskForm):
	#Registration form

	username = StringField('username_label', validators=[InputRequired(message="Username reuired")])
	password = PasswordField('password_label', validators=[InputRequired(message="Password reuired"),
		invalid_credentials])
	submit_button = SubmitField('Login')
