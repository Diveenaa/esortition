from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_wtf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
# csrf = CSRFProtect(app)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

