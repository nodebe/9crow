from flask import Blueprint, render_template, request, flash, redirect, url_for
from ncrow.users.forms import Register, ProfilePersonal, ProfileEmail, ProfilePhone, PasswordChange, BankAccount, Login
from ncrow.models import User, Account
from ncrow import db
from flask_login import current_user, login_user, login_required, logout_user
from passlib.hash import sha256_crypt as sha256


users = Blueprint('users', __name__)
ERROR = 'Something went wrong, try again later!'

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('users.userdashboard'))
	form = Register()
	if form.validate_on_submit():
		hashed_password = sha256.encrypt(str(form.password.data))
		try:
			user = User(fullname=form.full_name.data, username=form.username.data, email=form.email.data, password=hashed_password, vendor_status=int(form.vendor.data))
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
			return redirect(url_for('users.register'))
		else:
			db.session.add(user)
			balance = Balance(user_balance=user)
			db.session.add(balance)
			db.session.commit()
			login_user(user)
			flash('Account created successfully.', 'success')
			flash('Please complete your profile', 'info')
			return redirect(url_for('users.userprofile'))

	return render_template('signup.html', title='9crow - Sign up', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('users.userdashboard'))
	login_form = Login()
	if login_form.validate_on_submit():
		try:
			user = User.query.filter_by(email=login_form.email.data).first()
			if user and sha256.verify(login_form.password.data, user.password):
				login_user(user)
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('users.userdashboard'))
			else:
				flash('This user does not exist!', 'warning')
				return redirect(url_for('users.login'))
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
			return redirect(url_for('users.login'))
	return render_template('login.html', title='9crow - Login', login_form=login_form)

@users.route('/userprofile', methods=["GET", "POST"])
@users.route('/userprofile/<form_type>', methods=["POST", "GET"])
@login_required
def userprofile(form_type=''):
	personal_edit_form = ProfilePersonal()
	email_edit_form = ProfileEmail()
	phone_edit_form = ProfilePhone()
	password_edit_form = PasswordChange()

	if request.method == 'GET':
		# Inserting data from db into form fields
		personal_edit_form.full_name.data = current_user.fullname
		personal_edit_form.username.data = current_user.username
		personal_edit_form.address.data = current_user.address
		personal_edit_form.dob.data = current_user.dob
		personal_edit_form.city.data = current_user.city
		personal_edit_form.state.data = current_user.state
		personal_edit_form.country.data = current_user.country
		email_edit_form.email.data = current_user.email
		phone_edit_form.phone.data = current_user.phone

	# updating personal form values
	if form_type == 'personal' and personal_edit_form.validate_on_submit():
		try:
			current_user.fullname = personal_edit_form.full_name.data
			current_user.username = personal_edit_form.username.data
			current_user.address = personal_edit_form.address.data
			current_user.dob = personal_edit_form.dob.data
			current_user.city = personal_edit_form.city.data
			current_user.state = personal_edit_form.state.data
			current_user.country = personal_edit_form.country.data
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
		else:
			db.session.commit()
			flash('Personal details updated successfully.', 'success')
			return redirect(url_for('users.userprofile'))
	#updating email form value
	elif form_type == 'email' and email_edit_form.validate_on_submit():
		try:
			current_user.email = email_edit_form.email.data
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
		else:
			db.session.commit()
			flash('Email updated successfully.', 'success')
			return redirect(url_for('users.userprofile'))
	#updating phone form value
	elif form_type == 'phone' and phone_edit_form.validate_on_submit():
		try:
			current_user.phone = phone_edit_form.phone.data
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
		else:
			db.session.commit()
			flash('Phone number updated successfully.', 'success')
			return redirect(url_for('users.userprofile'))
	#updating user password
	elif form_type == 'password' and password_edit_form.validate_on_submit():
		hashed_password = sha256.encrypt(str(password_edit_form.newpassword.data))
		try:
			current_user.password = hashed_password
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
		else:
			db.session.commit()
			flash('Password updated successfully.', 'success')
			return redirect(url_for('users.userprofile'))

	return render_template('profile.html', title='Profile', personal_edit=personal_edit_form, email_edit=email_edit_form, phone_edit=phone_edit_form, password_edit=password_edit_form)

@users.route('/userprofile_bank_accounts', methods=['GET', 'POST'])
def userprofile_bank_accounts():
	bank_edit_form = BankAccount()

	if  bank_edit_form.validate_on_submit():
		try:
			new_account = Account(user_id=current_user.id, bank_name=bank_edit_form.bank_name.data, account_name=bank_edit_form.account_name.data, account_number=bank_edit_form.account_number.data, account_type=bank_edit_form.account_type.data)
		except Exception as e:
			flash(f'{ERROR} : {e}', 'warning')
		else:
			db.session.add(new_account)
			db.session.commit()
			flash('Bank Account added successfully.', 'success')
			return redirect(url_for('users.userprofile_bank_accounts'))

	return render_template('profile-bank-accounts.html', title='Bank Accounts', bank_edit=bank_edit_form)

@users.route('/profile_notifications')
def profile_notifications():

	return render_template('profile-notifications.html', title='Notifications')

@users.route('/delete_bank_account/<account_id>')
def delete_bank_account(account_id):
	try:
		account = Account.query.filter_by(id=account_id).first()
		db.session.delete(account)
		db.session.commit()
	except Exception as e:
		flash(f'{ERROR} : {e}', 'warning')
	else:
		flash('Account details deleted successfully.', 'success')
		return(redirect(url_for('users.userprofile_bank_accounts')))

	return(redirect(url_for('users.userprofile_bank_accounts')))

@users.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():

	return '<h1>So you forgot your password! What do you want me to do?</h1>'

@users.route('/userdashboard')
def userdashboard():

	return render_template('dashboard.html', title='User Dashboard')

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))