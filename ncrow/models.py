from ncrow import db, login_manager
from flask_login import UserMixin
from datetime import datetime as dt


@login_manager.user_loader
def load_user(user_id):
	'''This callback is used to reload the user object from the user ID stored in the session. 
	It should take the unicode ID of a user, and return the corresponding user object'''
	
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	fullname = db.Column(db.String(30))
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	phone = db.Column(db.String(15))
	password = db.Column(db.String(150), nullable=False)
	user_status = db.Column(db.String(10), default='member')	
	vendor_status = db.Column(db.Integer, default=0)
	rating = db.Column(db.String, default='0.0') # A list seperated by ';' is used here. all vendor ratings are in the list to be able to calculate the average
	rating_count = db.Column(db.Integer, default=0) # This increments by 1 anytime a vendor gets rated by a customer who bought something from him(the vendor)
	dob = db.Column(db.DateTime, default=dt.now())
	address = db.Column(db.String)
	city = db.Column(db.String)
	state = db.Column(db.String)
	store_name = db.Column(db.String, default='9crow services')
	country = db.Column(db.String, default='Nigeria')
	bank_accounts = db.relationship('Account', backref='bank_accounts', lazy=True)
	balance = db.relationship('Balance', backref='user_balance', uselist=False)
	vendor_transactions = db.relationship('Transaction', backref='vendor',foreign_keys='Transaction.vendor_id')
	user_transactions = db.relationship('Transaction', backref='buyer',foreign_keys='Transaction.buyer_id')
	withdraws_deposits = db.relationship('WithdrawDeposit', backref='user_withdraws_deposits')

class Account(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Connects to the account model to the user that owns the account
	bank_name = db.Column(db.String)
	account_name = db.Column(db.String)
	account_number = db.Column(db.String(11))
	account_type = db.Column(db.String(9)) # Personal or Business account
	account_status = db.Column(db.String(8), default='Pending')

class Balance(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	available = db.Column(db.Integer, default=0) # Increases when transaction is fulfilled and reduces when withdrawal takes place
	pending = db.Column(db.Integer, default=0) # Increases when customer pays using link and Reduces when transaction is fulfilled
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Connects to the balance model to the user that owns the balance

class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	transaction_id = db.Column(db.String(18), unique=True) # Generated using the token secrets. Do check before inserting
	amount = db.Column(db.Integer, default=0)
	description= db.Column(db.String)
	transaction_date = db.Column(db.DateTime)
	_vendor_picture = db.Column(db.String, default = None)
	_buyer_picture = db.Column(db.String, default = None)
	rating = db.Column(db.Integer, default=0)
	buyer_comment = db.Column(db.Text)
	vendor_comment = db.Column(db.Text)
	customer_fulfilled = db.Column(db.Integer, default=0)
	vendor_fulfilled = db.Column(db.Integer, default=0)


	@property
	def vendor_picture(self):

		return [picture for picture in self._vendor_picture.split(';')]

	@vendor_picture.setter
	def vendor_picture(self, pictures):
		for picture in pictures:
			if self._vendor_picture != None:
				self._vendor_picture += ';{}'.format(picture)
			else:
				self._vendor_picture = '{}'.format(picture)


	@property
	def buyer_picture(self):

		return [picture for picture in self._buyer_picture.split(';')]

	@buyer_picture.setter
	def buyer_picture(self, pictures):
		for picture in pictures:
			if self._buyer_picture != None:
				self._buyer_picture += ';{}'.format(picture)
			else:
				self._buyer_picture = '{}'.format(picture)

class WithdrawDeposit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	transaction_type = db.Column(db.String(11))
	transaction_id = db.Column(db.String(18))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	amount = db.Column(db.Integer, default=0)
	transaction_date = db.Column(db.DateTime)
	status = db.Column(db.String(9), default='pending')