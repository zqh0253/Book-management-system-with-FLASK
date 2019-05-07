from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
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

class ChangeBookForm(FlaskForm):
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

