from app import app, db
from models import User, Vehicle, Dealership, Review, Likes, Rating, UserVehicle, VehicleDealership
from datetime import datetime

# Flask setup
with app.app_context():
    # Create tables
    db.create_all()

    # Add sample users
    user1 = User(firstname='Rasmi', lastname='Noel', email='rasmi.Noel@gmail.com', password='password1')
    user2 = User(firstname='Abdullahi', lastname='Abass', email='abdullahi.abass@gmail.com', password='password2')
    user3 = User(firstname='Isaac', lastname='Mutiga', email='isaac.mutiga@gmail.com', password='password3')
    user4 = User(firstname='Bryan', lastname='Kiplangat', email='bryan.kiplangat@example.com', password='password4')
    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    # Add sample vehicles
    vehicle1 = Vehicle(make='Toyota', model='Camry', year=2020)
    vehicle2 = Vehicle(make='Honda', model='Civic', year=2019)

    db.session.add_all([vehicle1, vehicle2])
    db.session.commit()

    # Add sample dealerships
    dealership1 = Dealership(name='Dynamic Cruisers1', address='Mombasa', website='dynamic-cruisers.com', rating=4.5)
    dealership2 = Dealership(name='Dynamic Cruisers2', address='Nairobi', website='dynamic-cruisers.com', rating=3.8)

    db.session.add_all([dealership1, dealership2])
    db.session.commit()

    # Add sample reviews
    review1 = Review(title='Great Car', content='I love my new Camry!', date_posted=datetime.utcnow(), user=user1, vehicle=vehicle1)
    review2 = Review(title='Smooth Ride', content='The Civic is a smooth ride.', date_posted=datetime.utcnow(), user=user2, vehicle=vehicle2)

    db.session.add_all([review1, review2])
    db.session.commit()

    # Add sample likes
    like1 = Likes(user=user1, vehicle=vehicle1)
    like2 = Likes(user=user2, vehicle=vehicle2)

    db.session.add_all([like1, like2])
    db.session.commit()

    # Add sample ratings
    rating1 = Rating(rating=4, user=user1, dealership=dealership1)
    rating2 = Rating(rating=3, user=user2, dealership=dealership2)

    db.session.add_all([rating1, rating2])
    db.session.commit()

    print('Database seeded successfully!')
