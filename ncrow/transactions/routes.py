import secrets
from datetime import datetime as dt
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from ncrow import db
from ncrow.models import User, Transaction
from ncrow.transactions.forms import RequestForm
from flask_login import current_user, login_user, login_required
from passlib.hash import sha256_crypt as sha256


transactions = Blueprint('transactions', __name__)
ERROR = 'Something went wrong, try again later!'

@transactions.route('/withdraw')
@login_required
def withdraw():

	return render_template('withdraw-money.html', title='Withdraw')

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