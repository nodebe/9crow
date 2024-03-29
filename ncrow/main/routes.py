from flask import Blueprint, render_template, request, flash, redirect, url_for



main = Blueprint('main', __name__)
ERROR = 'Something went wrong, try again later!'

@main.route('/')
def index():
	return render_template('index.html', title='Securing every purchase')

@main.route('/fees')
def fees():
	
	return render_template('fees.html', title='Fees')

@main.route('/contactus')
def contactus():
	
	return render_template('contact-us.html', title='Contact us')

@main.route('/aboutus')
def aboutus():

	return render_template('about-us.html', title='About us')

@main.route('/help')
def help():

	return render_template('help.html', title='Help')