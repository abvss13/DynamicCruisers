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
