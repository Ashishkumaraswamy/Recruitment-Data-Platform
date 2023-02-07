import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from .module.models import *

# Load environment variables
dotenv_path = os.path.dirname(os.path.abspath(__file__))+'\.env'  
load_dotenv(dotenv_path)  

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder='../templates', static_folder='../static')
# CORS(app)

# JWT
app.config['SECRET_KEY'] = 'my secret key'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('MYSQL_USERNAME')}:{os.getenv('MYSQL_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

# db = SQLAlchemy(app)
ma = Marshmallow(app)

db.init_app(app)
with app.app_context():
    db.create_all()
