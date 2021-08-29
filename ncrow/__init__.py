from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from ncrow.config import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager =  LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from ncrow.models import *


from ncrow.users.routes import users
from ncrow.main.routes import main
from ncrow.transactions.routes import transactions

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(transactions)


db.create_all()
db.session.commit()