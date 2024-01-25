<<<<<<< HEAD
from app import db, User, Vehicle, Dealership, Review, Likes, Rating
from faker import Faker
from datetime import datetime

fake = Faker()

def generate_fake_user():
    return User(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        password="password"  # Replace with a hashed password in a real application
    )

def generate_fake_vehicle():
    return Vehicle(
        make=fake.word(),
        model=fake.word(),
        year=fake.year(),
        availability=fake.boolean(),
        numbers_available=fake.random_int(min=1, max=10),
        likes=fake.random_int(min=0, max=100),
        image=fake.image_url()
    )

def generate_fake_dealership():
    return Dealership(
        name=fake.company(),
        address=fake.address(),
        website=fake.url(),
        rating=fake.random.uniform(1.0, 5.0)
    )

def generate_fake_review(user, vehicle):
    return Review(
        title=fake.sentence(),
        content=fake.paragraph(),
        date_posted=datetime.utcnow(),
        user=user,
        vehicle=vehicle
    )

def generate_fake_likes(user, vehicle):
    return Likes(
        user=user,
        vehicle=vehicle
    )

def generate_fake_rating(user, dealership):
    return Rating(
        rating=fake.random_int(min=1, max=5),
        user=user,
        dealership=dealership
    )

def seed_database():
    db.create_all()

    # Create fake users
    users = [generate_fake_user() for _ in range(10)]
    db.session.add_all(users)
    db.session.commit()

    # Create fake vehicles
    vehicles = [generate_fake_vehicle() for _ in range(10)]
    db.session.add_all(vehicles)
    db.session.commit()

    # Create fake dealerships
    dealerships = [generate_fake_dealership() for _ in range(5)]
    db.session.add_all(dealerships)
    db.session.commit()

    # Create fake reviews, likes, and ratings
    for user in users:
        vehicle = fake.random_element(vehicles)
        dealership = fake.random_element(dealerships)

        review = generate_fake_review(user, vehicle)
        likes = generate_fake_likes(user, vehicle)
        rating = generate_fake_rating(user, dealership)

        db.session.add_all([review, likes, rating])

    db.session.commit()

if __name__ == "__main__":
    seed_database()
=======
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
>>>>>>> 4d11d9cae84240939581ac1f92db976ea318011b
