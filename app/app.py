from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError #for handling database errors
from flask import jsonify, request, make_response
from flask_restful import Api, Resource


from models import db, User, Vehicle, Dealership, Review, Rating, Likes, UserVehicle, VehicleDealership

#app configuration
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


#database initialization and migration
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

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
# Dealerships Routes
class DealershipsResource(Resource):
    def get(self):
        dealerships = Dealership.query.all()
        dealerships_list = [
            {
                "id": dealership.id,
                "name": dealership.name,
                "address": dealership.address,
                "website": dealership.website,
                "rating": dealership.rating,
                # Include other dealership attributes as needed
            } for dealership in dealerships
        ]
        return jsonify(dealerships_list)

    def post(self):
        data = request.get_json()

        dealership = Dealership(
            name=data['name'],
            address=data['address'],
            website=data['website'],
            rating=data['rating']
        )

        db.session.add(dealership)
        db.session.commit()

        dealership_dict = {
            "id": dealership.id,
            "name": dealership.name,
            "address": dealership.address,
            "website": dealership.website,
            "rating": dealership.rating,
        }

        response = make_response(jsonify(dealership_dict), 201)  # 201 Created
        return response

api.add_resource(DealershipsResource, '/dealerships', endpoint='dealerships')
api.add_resource(DealershipsResource, '/dealerships/<int:dealership_id>', endpoint='dealership')

# Vehicles Routes
class VehiclesResource(Resource):
    def get(self, id=None):
        if id is None:
            #then get all vehicles
            vehicles = Vehicle.query.all()
            if vehicles:
                try:
                    vehicles_list = [
                        {
                            "id": vehicle.id,
                            "make": vehicle.make,
                            "model": vehicle.model,
                            "year": vehicle.year,
                            "availability": vehicle.availability,
                            "numbers_available": vehicle.numbers_available,
                            "likes": vehicle.likes,
                            "image": vehicle.image,
                            # Include other vehicle attributes as needed
                        } for vehicle in vehicles
                    ]
                    response = make_response(
                        jsonify(vehicles_list),
                        200
                    )
                except Exception as e:
                    print(f"Caught an exception: {e}") 
                    response = make_response(
                        jsonify({"error": f"{e}"}),
                        404
                    )  
            else:
                response = make_response(
                    jsonify({"error": f"Vehicles not found"}),
                    404
                )

            return response 
        else:
            # route has vehicle id, so get vehicle by id
            #/vehicles/<int: veicle_id>
            vehicle = Vehicle.query.filter_by(id=id).first()
            if vehicle:
                vehicles_dict = {
                    "id": vehicle.id,
                    "make": vehicle.make,
                    "model": vehicle.model,
                    "year": vehicle.year,
                    "availability": vehicle.availability,
                    "numbers_available": vehicle.numbers_available,
                    "likes": vehicle.likes,
                    "image": vehicle.image,
                }
                response = make_response(
                    jsonify(vehicles_dict),
                    200
                )
            else:
                response = make_response(
                    jsonify({"error": f"Vehicle id {id} not found"}),
                    404
                )
            return response 

    def post(self):
        
            data = request.get_json()

            required_fields = ['make', 'model', 'year']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                error_message = f"Missing keys: {','.join(missing_fields)}"
                return jsonify({"error": error_message}), 400
               
            vehicle = Vehicle(
                make=data['make'],
                model=data['model'],
                year=data['year'],
                availability=bool(data.get('availability', False)),
                numbers_available=data.get('numbers_available', 1),
                likes=data.get('likes', 0),
                image=data.get('image')
            )

            db.session.add(vehicle)
            db.session.commit()

            updated_vehicle = Vehicle.query.get(vehicle.id)
            vehicle_dict = {
               "id": updated_vehicle.id,
               "make": updated_vehicle.make,
               "model": updated_vehicle.model,
               "year": updated_vehicle.year,
               "availability": updated_vehicle.availability,
               "numbers_available": updated_vehicle.numbers_available,
               "likes": updated_vehicle.likes,
               "image": updated_vehicle.image,
            }

            response = make_response(jsonify(vehicle_dict), 201)  # 201 Created
            return response
        
       
      

api.add_resource(VehiclesResource, '/vehicles', endpoint='vehicles')
api.add_resource(VehiclesResource, '/vehicles/<int:id>', endpoint='vehicle')

# Reviews Routes
class ReviewsResource(Resource):
    def get(self):
        reviews = Review.query.all()
        reviews_list = [
            {
                "id": review.id,
                "title": review.title,
                "content": review.content,
                "date_posted": review.date_posted.isoformat(),
                "user_id": review.user_id,
                "vehicle_id": review.vehicle_id,
                # Include other review attributes as needed
            } for review in reviews
        ]
        return jsonify(reviews_list)

    def post(self):
        data = request.get_json()

        review = Review(
            title=data['title'],
            content=data['content'],
            user_id=data['user_id'],
            vehicle_id=data['vehicle_id']
        )

        db.session.add(review)
        db.session.commit()

        review_dict = {
            "id": review.id,
            "title": review.title,
            "content": review.content,
            "date_posted": review.date_posted.isoformat(),
            "user_id": review.user_id,
            "vehicle_id": review.vehicle_id,
        }

        response = make_response(jsonify(review_dict), 201)  # 201 Created
        return response

api.add_resource(ReviewsResource, '/reviews', endpoint='reviews')
api.add_resource(ReviewsResource, '/reviews/<int:review_id>', endpoint='review')

if __name__ == '__main__':
    app.run(port=5555)
