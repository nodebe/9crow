from ncrow.models import User
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, DateField
from wtforms.fields.html5 import EmailField, TelField, URLField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import sha256_crypt as sha256

STATES = [('Abia'), ('Adamawa'), ('Akwa Ibom'), ('Anambra'), ('Bauchi'), ('Bayelsa'), ('Benue'), ('Borno'), ('Cross River'), ('Delta'), ('Ebonyi'), ('Edo'), ('Ekiti'), ('Enugu'), ('Gombe'), ('Imo'), ('Jigawa'), ('Kaduna'), ('Kano'), ('Katsina'), ('Kebbi'), ('Kogi'), ('Kwara'), ('Lagos'), ('Nasarawa'), ('Niger'), ('Ogun'), ('Ondo'), ('Osun'), ('Oyo'), ('Plateau'), ('Rivers'), ('Sokoto'), ('Taraba'), ('Yobe'), ('Zamfara'), ('FCT')]

COUNTRIES = [('Nigeria')]

class Register(FlaskForm):
	full_name = StringField('Full Name', validators=[InputRequired('Fill in your fullname')] )	
	username = StringField('Username', validators=[InputRequired('Fill in a username'), Length(min=3)] )
	email = EmailField('Email', validators=[InputRequired('Fill in a valid Email')])
	password = PasswordField('Password', validators=[InputRequired('Fill in a strong password'), Length(min=6,message='Password must be more than 6 characters')])
	confirm = PasswordField('Repeat Password', validators=[EqualTo('password', message = 'Passwords must match')])
	vendor = BooleanField('')
	agree = BooleanField('', validators=[InputRequired()], default='checked')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists!')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists!')

class ProfilePersonal(FlaskForm):
	full_name = StringField('Full Name', validators=[InputRequired('Fill in your fullname')] )	
	username = StringField('Username', validators=[InputRequired('Fill in a username'), Length(min=3)] )
	dob = DateField('Date of Birth')
	address = StringField('Address', validators=[InputRequired('Fill in your Address'), Length(max=120)])
	city = StringField('City', validators=[Length(max=15)])
	state = SelectField('State', choices=STATES, validators=[InputRequired('Select a state')])
	country = SelectField('Country', choices=COUNTRIES, validators=[InputRequired('Select a country')])

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user and user!=current_user:
			raise ValidationError('Username already exists!')

class ProfileEmail(FlaskForm):
	email = EmailField('Email ID', validators=[InputRequired('Fill in a valid Email')])

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user and user!=current_user:
			raise ValidationError('Email already exists!')

class ProfilePhone(FlaskForm):
	phone = TelField('Mobile', validators=[InputRequired('Fill in a valid Phone Number')])

class PasswordChange(FlaskForm):
	oldpassword = PasswordField('Enter Current Password:', validators = [InputRequired()])
	newpassword = PasswordField('Enter New Password:', validators = [InputRequired('Fill in a strong password'), Length(min = 6, message = 'Password must be more than 6 characters')])
	confirm = PasswordField('Confirm New Password:', validators = [EqualTo('newpassword', message = 'Passwords must match')])


	def validate_oldpassword(self, oldpassword):
		if not sha256.verify(oldpassword.data, current_user.password):
			raise ValidationError('Password is not correct!')