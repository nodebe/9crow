from flask import Blueprint, render_template, request, flash, redirect, url_for
from ncrow.models import User
from ncrow import db
from flask_login import current_user, login_user, login_required
from passlib.hash import sha256_crypt as sha256


transactions = Blueprint('transactions', __name__)
ERROR = 'Something went wrong, try again later!'

@transactions.route('/withdraw')
@login_required
def withdraw():

	return render_template('withdraw-money.html', title='Withdraw')
