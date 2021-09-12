from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from ncrow.config import app
from flask_avatars import Avatars

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager =  LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
avatars = Avatars(app)

from ncrow.models import *

# @login_manager.user_loader
# def load_user(user_id):
# 	'''This callback is used to reload the user object from the user ID stored in the session. 
# 	It should take the unicode ID of a user, and return the corresponding user object'''
	
# 	return User.query.get(int(user_id))

from ncrow.users.routes import users
from ncrow.main.routes import main
from ncrow.transactions.routes import transactions

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(transactions)


db.create_all()
db.session.commit()