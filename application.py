from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256

from wtform_fields import *
from models import *

#Configure App
app = Flask(__name__)
app.secret_key = 'complicated_key'

#Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sxygwgsgwsshyu:abe58905c1f152b54874ca679b5cb00eb2ca9fa198ef0e659e7afd87a083ff54@ec2-34-200-72-77.compute-1.amazonaws.com:5432/dd5itlspee4qcv'

db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

	reg_form = RegistrationForm()

	if reg_form.validate_on_submit():
		username = reg_form.username.data
		password = reg_form.password.data

		#hash the password for security purposes by adding a salt
		hashed_password = pbkdf2_sha256.hash(password)

		user = Users(username=username, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))

	return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	
	login_form = LoginForm()

	#Allow user to login if validation success
	if login_form.validate_on_submit():
		return "Logged In"

	return render_template("login.html", form=login_form)

if __name__== "__main__":
	app.run(debug=True)