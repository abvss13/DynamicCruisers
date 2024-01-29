from flask import Flask, session
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError #for handling database errors
from flask import jsonify, request, make_response
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash



from models import db, User, Vehicle, Dealership, Review, Rating, Likes, UserVehicle, VehicleDealership

#app configuration
app = Flask(__name__)
CORS(app)

#set a key for session management
app.secret_key = b'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


#database initialization and migration
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def index():
    response = make_response(jsonify({'message': 'Welcome to the Car Dealership API'}), 200)

    #set a cookie in the response
    response.set_cookie('User_id', '123', max_age=3000)#set a user_id cookie for 1 hr
    return response


#mock user authentication function
def authenticate_user(email, password):
    user = User.query.filter_by(email=email, password=password).first()
    return user is not None


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    #check if the required fields are present in the request data
    required_fields = ['email', 'password']
    if any(field not in data for field in required_fields):
        return {"error": "Missing required fields"}, 400
    
    email = data['email']
    password = data['password']

    #Authenticate the user
    user = User.query.filter_by(email=email).first()
    # hashed_password = generate_password_hash(data['password'], method='sha256')

    if user and check_password_hash(user.password, data['password']):
        #set a session cookie to indicate that the user is authenticated
        session['authenticated_user'] = email
        print("logged in")
        return jsonify({"message": "Login successful"}), 200
    else:
        #an error message for an unsuccessful login
        print("login error") 
        return jsonify({"error": "Invalid credentials"}), 401
    
@app.route('/protected')
def protected_route():
    #check if the user is authenticated based on the session cookie
    if 'authenticated_user' in session:
        email = session['authenticated_user']
        return jsonify({"message": f"Hello, {email}! This is a protected route."}), 200
    else:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

@app.route('/logout')
def logout():
    #Clear the session cookie to log the user out
    session.pop('authenticated_user', None)
    return jsonify({"Message": "Logout successful"}), 200


class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is not None:
            return self.get_single_user(user_id)


        users = User.query.all()
        users_dict = [
            {
                "id": user.id,
                "first_name": user.firstname,
                "last_name": user.lastname,
                "email": user.email,
                "vehicles_owned": user.vehicles_owned,
                "reviews": self.serialize_reviews(user.reviews),
                "password": user.password
            }
            for user in users
        ]
        response = make_response(
            jsonify(users_dict),
            200
        )
        return response
    
    def serialize_reviews(self, reviews):
        return [
            {
                "id": review.id,
                "content": review.content
            }
            for review in reviews
        ]
    
    def get_single_user(self, user_id):
        user = User.query.get(user_id)
        if user:
            user_dict = {
                "id": user.id,
                "first_name": user.firstname,
                "last_name": user.lastname,
                "email": user.email,
                "vehicles_owned": user.vehicles_owned,
                "reviews": self.serialize_reviews(user.reviews),
                "password": user.password
            }
            response = make_response(
                 jsonify(user_dict),
                 200
            )
            return response
        else:
            return jsonify({"error": f"User with id {user_id} not found"}), 404
        
    def post(self):
        data = request.get_json()

        # Check if required fields are present in the request data
        required_fields = ['name', 'address', 'website']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            error_message = f"Missing keys: {','.join(missing_fields)}"
            return {"error": error_message}, 400

        # Create a new dealership instance
        new_dealership = Dealership(
            name=data['name'],
            address=data['address'],
            website=data['website']
            # Add other fields as needed
        )

        # Add the new dealership to the database
        db.session.add(new_dealership)
        db.session.commit()

        # Return the newly created dealership as a response
        dealership_data = {
            "id": new_dealership.id,
            "name": new_dealership.name,
            "address": new_dealership.address,
            "website": new_dealership.website
            # Add other fields as needed
        }

        response = make_response(jsonify(dealership_data), 201)  # 201 Created
        return response
    
    
    #delete a user
    def delete(self, user_id):
        # Get the user by ID
        user = User.query.get(user_id)

        # Check if the user exists
        if user:
            # Remove the user from the database
            db.session.delete(user)
            db.session.commit()

            return jsonify({"message": f"User with ID {user_id} has been deleted"}), 200
        else:
            return jsonify({"error": f"User with ID {user_id} not found"}), 404


    
api.add_resource(UserResource, '/users', endpoint='users')
api.add_resource(UserResource, '/users/<int:user_id>', endpoint='user')



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

    
    #delete for the vehicles
    def delete(self, id):
        vehicle = Vehicle.query.get(id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return make_response(jsonify({"message": f"Vehicle with id {id} deleted"}), 200)
        else:
            return make_response(jsonify({"error": f"Vehicle with id {id} not found"}), 404)
        


api.add_resource(VehiclesResource, '/vehicles', endpoint='vehicles')
api.add_resource(VehiclesResource, '/vehicles/<int:id>', endpoint='vehicle')


class DealershipsResource(Resource):
    def get(self, id=None):
        if id is None:
            # Get all dealerships
            dealerships = Dealership.query.all()
            if dealerships:
                try:
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
                    response = make_response(
                        jsonify(dealerships_list),
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
                    jsonify({"error": "Dealerships not found"}),
                    404
                )

            return response
        else:
            # Get dealership by id
            dealership = Dealership.query.filter_by(id=id).first()
            if dealership:
                dealership_dict = {
                    "id": dealership.id,
                    "name": dealership.name,
                    "address": dealership.address,
                    "website": dealership.website,
                    "rating": dealership.rating,
                    # Include other dealership attributes as needed
                }
                response = make_response(
                    jsonify(dealership_dict),
                    200
                )
            else:
                response = make_response(
                    jsonify({"error": f"Dealership id {id} not found"}),
                    404
                )
            return response
        
    #add a post for the dealerships
    def post(self):
        data = request.get_json()

        required_fields = ['name', 'address', 'website', 'rating']  
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            error_message = f"Missing keys: {','.join(missing_fields)}"
            return {"error": error_message}, 400

        
        dealership = Dealership(
            name=data['name'],
            address=data['address'],
            website=data['website'],
            rating=data['rating'],
            # Include other dealership attributes as needed
        )

        db.session.add(dealership)
        db.session.commit()

        updated_dealership = Dealership.query.get(dealership.id)
        dealership_dict = {
            "id": updated_dealership.id,
            "name": updated_dealership.name,
            "address": updated_dealership.address,
            "website": updated_dealership.website,
            "rating": updated_dealership.rating,
            # Include other dealership attributes as needed
        }

        response = make_response(jsonify(dealership_dict), 201)  # 201 Created
        return response
    
    #deletion of dealerships
    def delete(self, id):
        dealership = Dealership.query.get(id)

        if dealership:
            try:
                db.session.delete(dealership)
                db.session.commit()
                return {"message": f"Dealership id {id} deleted successfully"}, 200
            except Exception as e:
                db.session.rollback()
                return {"error": f"Failed to delete dealership: {e}"}, 500
        else:
            return {"error": f"Dealership id {id} not found"}, 404

            
    
# Todo
# add rating information when getting dealerships
api.add_resource(DealershipsResource, '/dealerships', endpoint='dealerships')
api.add_resource(DealershipsResource, '/dealerships/<int:id>', endpoint='dealership')


# Dealership ratings Routes
class RatingsResource(Resource):
    def get(self, id=None):
        if id is None:
            # Get all ratings
            ratings = Rating.query.all()
            if ratings:
                try:
                    ratings_list = [
                        {
                            "id": rating.id,
                            "rating": rating.rating,
                            "user_id": rating.user_id,
                            "user_firstname": rating.user.firstname,  # Include user details as needed
                            "user_lastname": rating.user.lastname,
                            "dealership_id": rating.dealership_id,
                            "dealership_name": rating.dealership.name,  # Include dealership details as needed
                        } for rating in ratings
                    ]
                    response = make_response(
                        jsonify(ratings_list),
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
                    jsonify({"error": "Ratings not found"}),
                    404
                )

            return response
        else:
            # Get rating by id
            rating = Rating.query.filter_by(id=id).first()
            if rating:
                rating_dict = {
                    "id": rating.id,
                    "rating": rating.rating,
                    "user_id": rating.user_id,
                    "user_firstname": rating.user.firstname,  # Include user details as needed
                    "user_lastname": rating.user.lastname,
                    "dealership_id": rating.dealership_id,
                    "dealership_name": rating.dealership.name,  # Include dealership details as needed
                }
                response = make_response(
                    jsonify(rating_dict),
                    200
                )
            else:
                response = make_response(
                    jsonify({"error": f"Rating id {id} not found"}),
                    404
                )
            return response

api.add_resource(RatingsResource, '/ratings', endpoint='ratings')
api.add_resource(RatingsResource, '/ratings/<int:id>', endpoint='rating')

# UserVehicles Routes
class UserVehiclesResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            # Get all user vehicles
            user_vehicles = UserVehicle.query.all()
            if user_vehicles:
                try:
                    user_vehicles_list = [
                        {
                            "user_id": user_vehicle.user_id,
                            "vehicle_id": user_vehicle.vehicle_id,
                            "vehicle_make": user_vehicle.vehicle.make,  # Include vehicle details as needed
                            "vehicle_model": user_vehicle.vehicle.model,
                            "vehicle_year": user_vehicle.vehicle.year,
                        } for user_vehicle in user_vehicles
                    ]
                    response = make_response(
                        jsonify(user_vehicles_list),
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
                    jsonify({"error": "User vehicles not found"}),
                    404
                )

            return response
        else:
            # Get user vehicles by user_id
            user_vehicles = UserVehicle.query.filter_by(user_id=user_id).all()
            if user_vehicles:
                try:
                    user_vehicles_list = [
                        {
                            "user_id": user_vehicle.user_id,
                            "vehicle_id": user_vehicle.vehicle_id,
                            "vehicle_make": user_vehicle.vehicle.make,  # Include vehicle details as needed
                            "vehicle_model": user_vehicle.vehicle.model,
                            "vehicle_year": user_vehicle.vehicle.year,
                        } for user_vehicle in user_vehicles
                    ]
                    response = make_response(
                        jsonify(user_vehicles_list),
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
                    jsonify({"error": f"User id {user_id} not found or has no associated vehicles"}),
                    404
                )
            return response

api.add_resource(UserVehiclesResource, '/user_vehicles', endpoint='user_vehicles')
api.add_resource(UserVehiclesResource, '/user_vehicles/<int:user_id>', endpoint='user_vehicle')

class DealershipVehiclesResource(Resource):
    def get(self):
        # Get vehicles belonging to a dealership by dealership_id
        dealership_vehicles = VehicleDealership.query.filter_by(dealership_id=dealership_id).all()
        if dealership_vehicles:
            try:
                dealership_vehicles_list = [
                    {
                        "dealership_id": dealership_vehicle.dealership_id,
                        "vehicle_id": dealership_vehicle.vehicle_id,
                        "vehicle_make": dealership_vehicle.vehicle.make,  # Include vehicle details as needed
                        "vehicle_model": dealership_vehicle.vehicle.model,
                        "vehicle_year": dealership_vehicle.vehicle.year,
                    } for dealership_vehicle in dealership_vehicles
                ]
                response = make_response(
                    jsonify(dealership_vehicles_list),
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
                jsonify({"error": f"Dealership id {dealership_id} not found or has no associated vehicles"}),
                404
            )
        return response

api.add_resource(DealershipVehiclesResource, '/dealership_vehicles/<int:dealership_id>', endpoint='dealership_vehicle')



# Reviews Routes
class ReviewsResource(Resource):
    def get(self, vehicle_id=None):
        if vehicle_id is not None:
            # Get reviews by vehicle_id
            reviews = Review.query.filter_by(vehicle_id=vehicle_id).all()
            if reviews:
                try:
                    reviews_list = [
                        {
                            "id": review.id,
                            "title": review.title,
                            "content": review.content,
                            "date_posted": review.date_posted.isoformat(),
                            "user_id": review.user_id,
                            "user_firstname": review.user.firstname,
                            "user_lastname": review.user.lastname,
                            "vehicle_id": review.vehicle_id,
                            "vehicle_make": review.vehicle.make,
                            "vehicle_model": review.vehicle.model,
                            "vehicle_year": review.vehicle.year,
                        } for review in reviews
                    ]
                    response = make_response(
                        jsonify(reviews_list),
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
                    jsonify({"error": f"No reviews found for vehicle id {vehicle_id}"}),
                    404
                )
        else:
            # Get all reviews
            reviews = Review.query.all()
            if reviews:
                try:
                    reviews_list = [
                        {
                            "id": review.id,
                            "title": review.title,
                            "content": review.content,
                            "date_posted": review.date_posted.isoformat(),
                            "user_id": review.user_id,
                            "user_firstname": review.user.firstname,
                            "user_lastname": review.user.lastname,
                            "vehicle_id": review.vehicle_id,
                            "vehicle_make": review.vehicle.make,
                            "vehicle_model": review.vehicle.model,
                            "vehicle_year": review.vehicle.year,
                        } for review in reviews
                    ]
                    response = make_response(
                        jsonify(reviews_list),
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
                    jsonify({"error": "No reviews found"}),
                    404
                )

        return response



    #get review by id
    def get_review(self, vehicle_id):
    # Get reviews by vehicle_id
        reviews = Review.query.filter_by(vehicle_id=vehicle_id).all()
        if reviews:
            try:
                reviews_list = [
                    {
                        "id": review.id,
                        "title": review.title,
                        "content": review.content,
                        "date_posted": review.date_posted.isoformat(),
                        "user_id": review.user_id,
                        "user_firstname": review.user.firstname,  # Include user details as needed
                        "user_lastname": review.user.lastname,
                        "vehicle_id": review.vehicle_id,
                        "vehicle_make": review.vehicle.make,  # Include vehicle details as needed
                        "vehicle_model": review.vehicle.model,
                        "vehicle_year": review.vehicle.year,
                    } for review in reviews
                ]
                response = make_response(
                    jsonify(reviews_list),
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
                jsonify({"error": f"No reviews found for vehicle id {vehicle_id}"}),
                404
            )
        return response
    def post(self):
        data = request.get_json()

        #check if the required fields are present in the requested data
        required_fields = ['title', 'content', 'user_id', 'vehicle_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            error_message = f"Missing keys: {','.join(missing_fields)}"
            return {"error": error_message}, 400
        
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
    
    #create a delete for reviews
    def delete(self, vehicle_id):
        review = Review.query.get(vehicle_id)

        if review:
            try:
                db.session.delete(review)
                db.session.commit()
                return {"message": f"Review id {vehicle_id} deleted successfully"}, 200
            except Exception as e:
                db.session.rollback()
                return {"error": f"Failed to delete review: {e}"}, 500
        else:
            return {"error": f"Review id {vehicle_id} not found"}, 404

api.add_resource(ReviewsResource, '/reviews', endpoint='reviews')
api.add_resource(ReviewsResource, '/reviews/<int:vehicle_id>', endpoint='review')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
