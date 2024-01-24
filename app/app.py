from flask import Flask
from flask.cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, request, make_response

from models import db, User, Vehicle, Dealership, Review, Rating, Likes, UserVehicle, VehicleDealership

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    response = make_response(jsonify({'message': 'Welcome to the Car Dealership API'}), 200)
    return response

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_dict = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]