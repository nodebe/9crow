from flask import Blueprint, render_template, request, flash, redirect, url_for



main = Blueprint('main', __name__)
ERROR = 'Something went wrong, try again later!'

@main.route('/')
def index():
	return render_template('index.html', title='9Crow - Securing every purchase')

@main.route('/fees')
def fees():
	
	return render_template('fees.html', title='9crow - Fees')