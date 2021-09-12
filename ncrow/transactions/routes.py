import secrets
from datetime import datetime as dt
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from ncrow import db
from ncrow.models import User, Transaction, WithdrawDeposit
from ncrow.transactions.forms import RequestForm
from flask_login import current_user, login_user, login_required
from passlib.hash import sha256_crypt as sha256


transactions = Blueprint('transactions', __name__)
ERROR = 'Something went wrong, try again later!'

@transactions.route('/request_money', methods=['GET', 'POST'])
@login_required
def request_money():
	request_form = RequestForm()
	if request_form.validate_on_submit():
		transaction_id = secrets.token_hex(8)
		check_id = Transaction.query.filter_by(transaction_id=transaction_id).first()
		while check_id: #Checks if transaction id already exists in db
			transaction_id = secrets.token_hex(8)
		try:
			transaction = Transaction(vendor_id=current_user.id, transaction_id=transaction_id, amount=request_form.amount.data, description=request_form.description.data, transaction_date=dt.now())
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
		else:
			db.session.add(transaction)
			db.session.commit()
			return redirect(url_for('transactions.request_money_success', transaction_id=transaction.id))
	return render_template('request-money.html', title='Request Money', request_form=request_form)

@transactions.route('/request_money_success/<transaction_id>')
@login_required
def request_money_success(transaction_id):
	transaction = Transaction.query.filter_by(id=transaction_id).first()
	if transaction.vendor_id == current_user.id:

		return render_template('request-money-success.html', title='Request money success', transaction=transaction)
	else:
		abort(401)

@transactions.route('/pay/<transaction_id>')
@login_required
def deposit_money(transaction_id):
	transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()

	return render_template('deposit-money.html', transaction=transaction, title='Deposit money')

@transactions.route('/paystack_page/<transaction_id>')
@login_required
def paystack_page(transaction_id):
	transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
	if transaction.vendor == current_user:
		flash("You can't make a payment for your own transaction.", 'warning')
		return redirect(url_for('transactions.deposit_money', transaction_id=transaction.transaction_id))
	if transaction.buyer != None:
		flash("There is already a user for this transaction.", 'warning')
		return redirect(url_for('users.userdashboard'))
	
	return '<h1>Oya pay!</h1>'

@transactions.route('/withdrawal', methods=['GET','POST'])
@login_required
def withdrawal():
	bank_id = request.form.get('bankValue')
	if request.method == 'POST':
		if current_user.balance.available > 0:
			try:
				transaction_id = secrets.token_hex(8)
				check_id = WithdrawDeposit.query.filter_by(transaction_id=transaction_id).first()
				while check_id: #Checks if transaction id already exists in db
					transaction_id = secrets.token_hex(8)
				withdraw = WithdrawDeposit(transaction_type='Withdrawal',transaction_id=transaction_id,user_id=current_user.id,bank_id=bank_id,amount=current_user.balance.available,transaction_date=dt.now())
			except Exception as e:
				flash(f'{ERROR} : {e}', 'warning')
			else:
				current_user.balance.available = 0
				db.session.add(withdraw)
				db.session.commit()
				# flash('Your withdrawal has been queued. You will receive the amount in your account within 24 hours.', 'success')
				return redirect(url_for('transactions.withdrawal_success', transaction_id=withdraw.id))
		else:
			flash('Your balance is too low.', 'warning')

	return render_template('withdraw-money.html', title='Withdraw')


@transactions.route('/withdrawal_success/<transaction_id>')
@login_required
def withdrawal_success(transaction_id):
	transaction = WithdrawDeposit.query.filter_by(id=transaction_id).first()
	if transaction.user_id == current_user.id:
		return render_template('withdraw-money-success.html', title='Withdraw success', transaction=transaction)
	else:
		abort(401)