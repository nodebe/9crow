from flask_wtf import FlaskForm
from ncrow.models import User
from wtforms import BooleanField,IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange


class RequestForm(FlaskForm):
	amount = IntegerField('', validators=[InputRequired('Please fill in the amount.'), NumberRange(min=1000, max=5000000)])
	description = TextAreaField('Description', validators=[InputRequired(), Length(max=280)])
	agree = BooleanField('', validators=[InputRequired()], default='checked')
