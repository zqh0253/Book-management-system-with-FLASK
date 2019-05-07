from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	isadmin = db.Column(db.Boolean)

	card = db.relationship('Card', backref = 'user', lazy = 'dynamic')
	borrows = db.relationship('Borrow', backref = 'borrower', lazy = 'dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	bookname = db.Column(db.String(64), index = True, unique = True)
	remain = db.Column(db.Integer, index = True)
	type  = db.Column(db.String(32), index = True)
	author = db.Column(db.String(32), index = True)
	year = db.Column(db.Integer, index = True)
	borrows = db.relationship('Borrow', backref = 'borrowbook', lazy = 'dynamic')

	def __repr__(self):
		return '<Book {}>'.format(self.bookname)

class Card(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	borrow_num = db.Column(db.Integer)

class Borrow(db.Model):
	id =db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'))