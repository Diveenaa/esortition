from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_wtf import CSRFProtect

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# csrf = CSRFProtect(app)

db.init_app(app)


with app.app_context():
    from .models import User
    db.drop_all()
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    # user_id is the primary key
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

