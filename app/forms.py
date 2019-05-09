from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,  optional
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class AddBookForm(FlaskForm):
	bookname = StringField('Book\'s name', validators=[DataRequired()])
	type = StringField('Book\'s type', validators=[DataRequired()])
	author = StringField('Author', validators=[DataRequired()]) 
	year = IntegerField('Public Year', validators=[DataRequired()])
	amount = IntegerField('Amount', validators=[DataRequired()])
	submit = SubmitField('Execute')

	def validate_amount(self, amount):
		if amount.data <= 0:
			raise ValidationError('The amount of the book has to be a positive number.')

	def validate_year(self, year):
		if year.data<1000:
			raise ValidationError('Please input the right public year.')

class DelBookForm(FlaskForm):
	bookname = StringField('Book\'s name', validators=[DataRequired()])
	amount = IntegerField('Amount', validators=[DataRequired()])
	submit = SubmitField('Execute')

	def validate_amount(self, amount):
		if amount.data <= 0:
			raise ValidationError('The amount of the book has to be a positive number.')

class AddCardForm(FlaskForm):
	uid = IntegerField('User\' id', validators=[DataRequired()])
	ceil = IntegerField('The upper limit of number of borrowed books', validators=[DataRequired()])
	submit = SubmitField('Execute')

	def validate_borrow_num(self, ceil):
		if ceil.data <= 0:
			raise ValidationError('The upper limit has to be a positive number.')	

class DelCardForm(FlaskForm):
	uid = IntegerField('User\' id', validators=[DataRequired()])
	submit = SubmitField('Execute')

class BorrowBookForm(FlaskForm):
	mul = SelectMultipleField('', coerce=int)
	submit2 = SubmitField('Borrow')


class FindBookForm(FlaskForm):
	choices = [(1,'bookname'),(2,'author'),(3,'type'),(4,'year')]
	mul = SelectField('Type of info. you want to search by:', choices = choices, coerce = int)
	context = StringField('context', validators=[DataRequired()])
	submit1 = SubmitField('Search')

class ReturnBookForm(FlaskForm):
	mul = SelectMultipleField('Books you have borrowed:', coerce=int)
	submit = SubmitField('Return')
