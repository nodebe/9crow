from ncrow.models import User
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.fields.html5 import EmailField, TelField, URLField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import sha256_crypt as sha256


class Register(FlaskForm):
	full_name = StringField('Full Name', validators = [InputRequired('Fill in your fullname')] )	
	username = StringField('Username', validators = [InputRequired('Fill in a username'), Length(min = 3,max = 10)] )
	email = EmailField('Email', validators = [InputRequired('Fill in a valid Email')])
	password = PasswordField('Password', validators = [InputRequired('Fill in a strong password'), Length(min = 6, message = 'Password must be more than 6 characters')])
	confirm = PasswordField('Repeat Password', validators = [EqualTo('password', message = 'Passwords must match')])
	vendor = BooleanField('')
	agree = BooleanField('', validators = [InputRequired()], default='checked')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Email already exists!')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('Username already exists!')