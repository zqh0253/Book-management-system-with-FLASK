from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddBookForm, DelBookForm, AddCardForm, DelCardForm, BorrowBookForm, FindBookForm, ReturnBookForm
from flask_login import current_user, login_user
from app.models import User, Book, Card, Borrow
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	return render_template('index.html', title = 'Home', isadmin = current_user.isadmin)

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
		# next_page = request.args.get('next')
		# if not next_page or url_parse(next_page).netloc != '':
		# 	next_page = url_for('index')
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods = ['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form  = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html',title = 'Register', form = form)

def check_admin():
	if not current_user.is_authenticated:
		return 'login'
	elif not current_user.isadmin == True:
		return 'index'
	else:
		return ''
	'''NEED IMP'''

@app.route('/admin')
def admin():
	if check_admin()!='':
		return redirect(url_for(check_admin()))
	return render_template('admin.html')

@app.route('/admin_add_book', methods = ['GET','POST'])
def admin_add_book():
	check_admin()
	form = AddBookForm()
	if form.validate_on_submit():
		find_book = db.session.query(Book).filter_by(bookname = form.bookname.data).first()
		if find_book is None:
			book = Book(bookname = form.bookname.data, remain = form.amount.data, author = form.author.data, type = form.type.data, year = form.year.data)
			db.session.add(book)
		else:
			find_book.remain += form.amount.data
		db.session.commit()
		flash('Succeed to add books to the library!') 
	return render_template('admin_change_book.html', form = form , type = 'Add')

@app.route('/admin_del_book', methods = ['GET','POST'])
def admin_del_book():
	check_admin()
	form = DelBookForm()
	if form.validate_on_submit():
		find_book = db.session.query(Book).filter_by(bookname = form.bookname.data).first()
		if find_book is None or find_book.remain < form.amount.data:
			flash('Failed to Delete book from the library!')
			return redirect(url_for('admin_del_book'))
		else:
			find_book.remain -= form.amount.data
			if find_book.remain == 0:
				db.session.delete(find_book)
		db.session.commit()
		flash('Succeed to delete books to the library!') 
		return redirect(url_for('admin'))
	return render_template('admin_change_book.html', form = form , type = 'Delete')

@app.route('/admin_add_card', methods = ['GET','POST'])
def admin_add_card():
	check_admin()
	form = AddCardForm()
	if form.validate_on_submit():
		find_card = db.session.query(Card).filter_by(user_id = form.uid.data).first()
		find_user = db.session.query(User).filter_by(id = form.uid.data).first()
		if find_user is None:
			flash('Fail! No such user.')
		elif find_card is None:
			card = Card(user_id = form.uid.data, borrow_num = form.ceil.data)
			db.session.add(card)
			db.session.commit()
			flash('Succeed to add card for user {}'.format(form.uid.data))
		else:
			flash('The user already has a card!')
	return render_template('admin_add_card.html', form = form)

@app.route('/admin_del_card', methods = ['GET','POST'])
def admin_del_card():
	check_admin()
	form = DelCardForm()
	if form.validate_on_submit():
		find_card = db.session.query(Card).filter_by(user_id = form.uid.data).first()
		find_user = db.session.query(User).filter_by(id = form.uid.data).first()
		if find_user is None:
			flash('Fail! No such user.')
		elif find_card is None:
			flash('Fail! The user do not have a card already.')
		elif db.session.query(Borrow).filter_by(user_id = find_card.user_id).first()!=None:
			flash('Fail! The card cannot be deleted before all the borrowed books being returned.')
		else:
			db.session.delete(find_card)
			db.session.commit()
			flash('Succeed to delete the card.')
	return render_template('admin_del_card.html', form = form)

def check_user():
	if not current_user.is_authenticated:
		return 'login'
	elif current_user.isadmin == True:
		return 'admin'
	else:
		return ''

@app.route('/user')
def user():
	if check_user()!='':
		return redirect(url_for(check_user()))
	return render_template('user.html')

res = []
@app.route('/user_borrow_book', methods = ['GET','POST'])
def user_borrow_book():
	global res
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	card = db.session.query(Card).filter_by(user_id = current_user.id).first()
	if check_user()!='':
		return redirect(url_for(check_user()))
	if card == None:
		flash('You have not got a borrow card. Your id is {}, ask the admin to create a card for this id.'.format(current_user.id))
		return redirect(url_for('index'))
	form = FindBookForm()
	form2 = BorrowBookForm()
	if form.submit1.data and form.validate_on_submit():
		if form.mul.data == 1:
			res = db.session.query(Book).filter_by(bookname = form.context.data).all()
		elif form.mul.data == 2:
			res = db.session.query(Book).filter_by(author = form.context.data).all()
		elif form.mul.data == 3:
			res = db.session.query(Book).filter_by(type = form.context.data).all()
		else:
			res = db.session.query(Book).filter_by(year = int(form.context.data)).all()
	form2.mul.choices = [(book.id, book.bookname) for book in res]
	nonexistbook = []
	cannotborrow = []
	success = []
	if form2 and form2.submit2.data and form2.validate_on_submit():
		for bid in form2.mul.data: 
			book = db.session.query(Book).filter_by(id = bid).first()
			if book is None:
				nonexistbook.append(book.bookname+' ')
			elif card.borrow_num == 0:
				cannotborrow.append(book.bookname+' ')
			else:
				card.borrow_num -= 1
				book.remain -= 1
				success.append(book.bookname+' ')
				record = Borrow(book_id = book.id, user_id = current_user.id)
				db.session.add(record)
		if success!=[]:
			flash('Succeed to borrow books: {}'.format(''.join(success)))
		if nonexistbook!=[]:
			flash('Fail to borrow books for lack of remains in library: {}'.format(''.join(nonexistbook)))
		if cannotborrow!=[]:
			flash('Fail to borrow books for disability of your card: {}'.format(''.join(cannotborrow)))
		db.session.commit()
	return render_template('user_borrow_book.html', form = form, form2 = form2, res = res)


@app.route('/user_check_book', methods = ['GET','POST'])
def user_check():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	card = db.session.query(Card).filter_by(user_id = current_user.id).first()
	if check_user()!='':
		return redirect(url_for(check_user()))
	if card == None:
		flash('You have not got a borrow card. Your id is {}, ask the admin to create a card for this id.'.format(current_user.id))
		return redirect(url_for('index'))
	borrow_list = [x.book_id for x in db.session.query(Borrow).filter_by(user_id = card.user_id).all()]
	book_list = [db.session.query(Book).filter_by(id = x).first() for x in borrow_list]
	return render_template('user_check_book.html', book_list = book_list, num = card.borrow_num)

@app.route('/user_return_book', methods = ['GET','POST'])
def user_return_book():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	card = db.session.query(Card).filter_by(user_id = current_user.id).first()
	if check_user()!='':
		return redirect(url_for(check_user()))
	if card == None:
		flash('You have not got a borrow card. Your id is {}, ask the admin to create a card for this id.'.format(current_user.id))
		return redirect(url_for('index'))
	form = ReturnBookForm()
	res = db.session.query(Borrow).filter_by(user_id = current_user.id).all()
	if res != None:
		res.sort(key = lambda x:db.session.query(Book).filter_by(id = x.book_id).first().bookname)
	form.mul.choices = [(record.id, db.session.query(Book).filter_by(id = record.book_id).first().bookname) for record in res]
	if form.validate_on_submit():
		for record in form.mul.data:
			rec = db.session.query(Borrow).filter_by(id = record).first()
			db.session.delete(rec)
			db.session.query(Book).filter_by(id = rec.book_id).first().remain += 1
			db.session.query(Card).filter_by(user_id = rec.user_id).first().borrow_num += 1
		db.session.commit()
		flash('Succeed to return the books!')
		return redirect(url_for('user_return_book'))
	return render_template('user_return_book.html', form = form)