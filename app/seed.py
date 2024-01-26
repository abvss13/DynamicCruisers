from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Vehicle, Dealership, Review, Rating, Likes, UserVehicle, VehicleDealership
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

fake = Faker()

def seed_users():
    for _ in range(10):
        user = User(
            firstname=fake.unique.first_name(),
            lastname=fake.unique.last_name(),
            email=fake.unique.email(),
            password=fake.password()
        )
        db.session.add(user)

    db.session.commit()

def seed_vehicles():
    for _ in range(10):
        vehicle = Vehicle(
            make=fake.company(),
            model=fake.word(),
            year=fake.year(),
            availability=fake.boolean(),
            numbers_available=fake.random_int(min=1, max=10),
            likes=fake.random_int(min=0, max=100),
            image=fake.file_name()
        )
        db.session.add(vehicle)

    db.session.commit()

def seed_dealerships():
    for _ in range(5):
        dealership = Dealership(
            name=fake.company(),
            address=fake.address(),
            website=fake.url(),
            rating=fake.random_int(min=1, max=5)
        )
        db.session.add(dealership)

    db.session.commit()

def seed_reviews():
    users = User.query.all()
    vehicles = Vehicle.query.all()

    for _ in range(15):
        review = Review(
            title=fake.sentence(),
            content=fake.paragraph(),
            date_posted=fake.date_time_this_decade(),
            user=fake.random_element(elements=users),
            vehicle=fake.random_element(elements=vehicles)
        )
        db.session.add(review)

    db.session.commit()

def seed_likes():
    users = User.query.all()
    reviews = Review.query.all()
    vehicles = Vehicle.query.all()

    for _ in range(20):
        like = Likes(
            user=fake.random_element(elements=users),
            review=fake.random_element(elements=reviews),
            vehicle=fake.random_element(elements=vehicles)
        )
        db.session.add(like)

    db.session.commit()

def seed_ratings():
    users = User.query.all()
    dealerships = Dealership.query.all()

    for _ in range(5):
        rating = Rating(
            rating=fake.random_int(min=1, max=5),
            user=fake.random_element(elements=users),
            dealership=fake.random_element(elements=dealerships)
        )
        db.session.add(rating)

    db.session.commit()

def seed_user_vehicle():
    users = User.query.all()
    vehicles = Vehicle.query.all()

    for user in users:
        for _ in range(fake.random_int(min=1, max=5)):
            user_vehicle = UserVehicle(
                user=user,
                vehicle=fake.random_element(elements=vehicles)
            )
            db.session.add(user_vehicle)

    db.session.commit()

def seed_vehicle_dealership():
    vehicles = Vehicle.query.all()
    dealerships = Dealership.query.all()

    for vehicle in vehicles:
        for _ in range(fake.random_int(min=1, max=3)):
            vehicle_dealership = VehicleDealership(
                vehicle=vehicle,
                dealership=fake.random_element(elements=dealerships)
            )
            db.session.add(vehicle_dealership)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        try:
            seed_users()
            seed_vehicles()
            seed_dealerships()
            seed_reviews()
            seed_likes()
            seed_ratings()
            seed_user_vehicle()
            seed_vehicle_dealership()
            print("Database seeded successfully.")
        except SQLAlchemyError as e:
            print(f"Error seeding database: {str(e)}")
