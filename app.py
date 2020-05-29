import requests
import json
import flask
from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_bootstrap import Bootstrap


from wtform_fields import *
from models import *



#Configure App
app = Flask(__name__)
app.secret_key = 'complicated_key'

#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "VZiRw90zkVi3Ipbnxg2xA", "isbns": "0446679097"})

#Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nzgmhxdlwwdcec:efb4d0febc3f1a2838ecf81355174183828b4281cd91c6239f4ffc79d54d4dda@ec2-52-71-231-180.compute-1.amazonaws.com:5432/d70tk20n2eq526'
db = SQLAlchemy(app)
Bootstrap(app)

#Utilize flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
	return Users.query.get(int(id))

#Signup route
@app.route("/", methods=['GET'])
def index():
#	data2 = data['books'][0]
	return "The avereage rating is "
#	return render_template("index.html", form=reg_form)

@app.route("/api/<isbn>", methods=['GET'])
def isbn(isbn):
	#Queries to get correct book from database by isbn that is given from URL
	books = Books.query.all()
	book_object = Books.query.filter_by(isbn=isbn).first()
	
	#Parses the api rewuest to get rest of the data
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "VZiRw90zkVi3Ipbnxg2xA", "isbns": "{}".format(isbn)})
	data = res.json()
	data2 = data['books'][0]
	isbnB = data2['isbn']
	review_count = data2['reviews_count']
	avereage_score = data2['average_rating']
	
	#puts data into json format
	page_data = {
	 "title " : book_object.title,
	 "author " : book_object.author,
	 "year " : book_object.year,
	 "isbn " : isbnB,
	 "review_count " : review_count,
	 "avereage_score " : avereage_score,
	}

	#dumps data on page in json format
	return json.dumps(page_data)
	

#Signup route
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	search_form = SearchForm()

	if current_user.is_authenticated:
		return "You must log out to sign up"

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

	return render_template("signup.html", form=reg_form, search_form = search_form)

#Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
	search_form = SearchForm()

	if current_user.is_authenticated:
		return "You must log out to login up"

	login_form = LoginForm()


	#Allow user to login if validation success
	if login_form.validate_on_submit():
		user_object = Users.query.filter_by(username=login_form.username.data).first()
		login_user(user_object)
		return redirect(url_for('home'))

	return render_template("login.html", form=login_form, search_form = search_form)




"""-----------------------------------------These routes are for people who are logged in-------------------------------"""


#Home page (Must be logged in to view)
@app.route("/home", methods=['GET', 'POST'])
def home():
	search_form = SearchForm()

	if not current_user.is_authenticated:
		return "You must login to have access to this page"	
	username = current_user.username
	return render_template("home.html", username = username, search_form = search_form)

@app.route("/books/allbooks", methods=['GET', 'POST'])
def allbooks():
	search_form = SearchForm() 

	if not current_user.is_authenticated:
		return "You must login to have access to this page"	

	username = current_user.username
	
	books = Books.query.all()
	
	return render_template("books/allbooks.html", books=books, username = username, search_form = search_form)

@app.route("/books/<search>", methods=['GET', 'POST'])
def searchedbooks(search):
	search_form = SearchForm() 

	if flask.request.method == 'POST':
		if search_form.validate_on_submit():
			search = search_form.search.data
			print('I am inside of the loop X2')

	if not current_user.is_authenticated:
		return "You must login to have access to this page"	

	username = current_user.username

	all_books = Books.query.all()

	books = []
	for x in all_books:
		if search in x.title:
			print('I am inside of the loop X2')
			print(search)
			books.append(x)
		elif search in x.author:
			books.append(x)
		elif search in x.isbn:
			books.append(x)

	return render_template("books/searchedbooks.html", books=books, username = username, search_form = search_form)


@app.route("/book/<title>", methods=['GET', 'POST'])
def bookTitle(title):
	search_form = SearchForm()

	books = Books.query.filter_by(title=title).first()
	username = current_user.username
	review_form = ReviewForm()
	

	if not current_user.is_authenticated:
		return "You must login to have access to this page"

	if flask.request.method == 'POST':
	
		if review_form.validate_on_submit():
			comment = review_form.comment.data
			rating = review_form.rating.data
			owner_id = current_user.id
			book_id = books.isbn

			comment_exist = Reviews.query.filter_by(book_id=book_id, owner_id=owner_id).first()
			
			if comment_exist == None:
				review = Reviews(comment=comment, rating = rating, owner_id = owner_id, book_id = book_id)
				db.session.add(review)
				db.session.commit()
				return "Your comment has been recorded"
			else:
				return "You cannot comment on the same book twice"
	else:
		return render_template("books/bookresult.html", books=books, username = username, form = review_form, search_form = search_form)

@app.route("/logout", methods=['GET'])
def logout():
	search_form = SearchForm()

	logout_user()

	return"Logged out using flask login "


if __name__== "__main__":
	app.run(debug=True)


#	print('-----------------------')
#	print("Before anything ")
#	print('-----------------------')	