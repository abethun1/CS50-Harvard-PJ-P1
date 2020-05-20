from flask import Flask, render_template

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

		#CHeck if username exist
		user_object = Users.query.filter_by(username=username).first()
		if user_object:
			return "Someone already has that username"
		user = Users(username=username, password=password)
		db.session.add(user)
		db.session.commit()
		return "Form submitted and user added"

	return render_template("index.html", form=reg_form)

if __name__== "__main__":
	app.run(debug=True)