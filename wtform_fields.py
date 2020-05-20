from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
	#Registration form

	username = StringField('username_label', validators=[InputRequired("Username reuired"),
		Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
	password = PasswordField('password_label', validators=[InputRequired("Password reuired"),
		Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
	confirmation_password = PasswordField('confirmation_password_label', validators=[InputRequired("Password reuired"),
		EqualTo('password', message="Passwords must match")])
	submit_button = SubmitField('Create')