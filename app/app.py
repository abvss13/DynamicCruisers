from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError #for handling database errors
from flask import jsonify, request, make_response

from models import db, User, Vehicle, Dealership, Review, Rating, Likes, UserVehicle, VehicleDealership

#app configuration
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
#
#database initialization and migration
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    response = make_response(jsonify({'message': 'Welcome to the Car Dealership API'}), 200)
    return response

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_dict = [{'id': user.id,
                   'firstname': user.firstname,
                   'lastname': user.lastname,
                   'email': user.email,
                   'reviews': user.reviews,
                   'vehicles_owned': user.vehicles_owned,
                   'reviews': user.reviews } for user in users]
    response = make_response(jsonify(users_dict), 200)
    return response

@app.route('/dealerships', methods=['GET'])
def get_dealerships():
    dealerships = Dealership.query.all()
    dealerships_dict = [{'id': dealership.id,
                         'name': dealership.name,
                         'address': dealership.address,
                         'website': dealership.website,
                         'rating': dealership.rating,
                         'vehicles': dealership.vehicles } for dealership in dealerships]
    response = make_response(jsonify(dealerships_dict), 200)
    return response
