from flask import Blueprint, render_template, request, flash, redirect, url_for




users = Blueprint('users', __name__)
ERROR = 'Something went wrong, try again later!'

@users.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('signup.html', title='Sign up')