from flask import Blueprint, render_template, request, flash, redirect, url_for
from ncrow.users.forms import Register
from ncrow.models import User
from ncrow import db
from flask_login import current_user, login_user, login_required
from passlib.hash import sha256_crypt as sha256


users = Blueprint('users', __name__)
ERROR = 'Something went wrong, try again later!'

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('users.user_dashboard'))
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
			db.session.commit()
			login_user(user)
			flash('Account created successfully.', 'success')
			flash('Please complete your profile', 'info')
			return redirect(url_for('users.userprofile'))

	return render_template('signup.html', title='9crow - Sign up', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

	return render_template('login.html', title='9crow - Login')

@users.route('/userprofile')
def userprofile():

	return render_template('profile.html', title='Profile')