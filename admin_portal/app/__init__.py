from flask import Flask
from flask_login import LoginManager
import os

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
ADMIN_MGMT_API_GATEWAY_URL = API_GATEWAY_URL + "admin_mgmt_service/"
ELECTION_MGMT_API_GATEWAY_URL = API_GATEWAY_URL + "election_mgmt_service/"
VOTE_MANAGER_API = API_GATEWAY_URL + "voting/"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

