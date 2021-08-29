from flask import Flask
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'cbfhcjkIVdoGRwAUQkXXjcKJmXlfFdWcvJBpgtmUQTmtfZDCtZ'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') or 'postgresql://postgres:nodywelete1@localhost/9crowdb'
