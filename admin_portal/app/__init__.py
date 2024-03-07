from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_wtf import CSRFProtect
import os

# API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
# ADMIN_MGMT_API_GATEWAY_URL = API_GATEWAY_URL + "admin_mgmt_service/"
# ELECTION_MGMT_API_GATEWAY_URL = API_GATEWAY_URL + "election_mgmt_service/"

ADMIN_MGMT_API_GATEWAY_URL = "https://lobster-app-5oxos.ondigitalocean.app/admin-mgmt-service-image/"
ELECTION_MGMT_API_GATEWAY_URL = "https://lobster-app-5oxos.ondigitalocean.app/election-mgmt-service-image/"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
# csrf = CSRFProtect(app)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

