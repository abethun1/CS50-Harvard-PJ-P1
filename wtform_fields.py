from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import Users, Books, Reviews


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
	#Login form

	username = StringField('username_label', validators=[InputRequired(message="Username reuired")])
	password = PasswordField('password_label', validators=[InputRequired(message="Password reuired"),
		invalid_credentials])
	submit_button = SubmitField('Login')

class ReviewForm(Form):
	#Comment form
	comment = TextAreaField('comment_label', validators=[InputRequired(message="Something must be written here"),
		Length(min=1, max=150, message="Comment must be between 10 - 150 characters long")])
	rating = RadioField('Label', choices=[('1','1 *'),('2','2 *'),('3','3 *'),('4','4 *')])
	submit_button = SubmitField('SubmitField')

class SearchForm(Form):
	"""SearchForm"""
	search = StringField('search_label', validators=[InputRequired("Must type in something"),
		Length(min=2, message="This field requires a min of 5 charcaters to search")])
	submit_button = SubmitField('Search')
