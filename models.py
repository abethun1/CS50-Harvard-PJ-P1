from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(UserMixin, db.Model):
	#User Model
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)
	user_reviews = db.relationship('Reviews', backref='owner')

class Books(db.Model):
#	#Books Model
	__searchable__ = []

	isbn = db.Column(db.String(25), primary_key =True, unique=True)
	title = db.Column(db.String(80))
	author = db.Column(db.String(80))
	year = db.Column(db.Integer)
	book_reviews = db.relationship('Reviews', backref='reviews')

class Reviews(db.Model):
	#Reviews model

	id = db.Column(db.Integer, primary_key=True)
	comment = db.Column(db.String(140))
	rating = db.Column(db.Integer(), nullable=False) 
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	book_id = db.Column(db.Integer, db.ForeignKey('books.isbn'))



		