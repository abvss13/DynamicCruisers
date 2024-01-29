from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Vehicle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

fake = Faker()


def seed_database():
    with app.app_context():
        db.create_all()

        # Delete all data in the vehicles table
        Vehicle.query.delete()
        db.session.commit()

        # Seed vehicles with real-life data
        # Add more data or modify as needed
        real_life_vehicles = [
            Vehicle(make="Toyota", model="Camry", year=2022, availability=True, numbers_available=5,
                    image="toyota_camry.jpg"),
            Vehicle(make="Honda", model="Civic", year=2022, availability=True, numbers_available=8,
                    image="honda_civic.jpg"),
            Vehicle(make="Ford", model="Fusion", year=2022, availability=True, numbers_available=3,
                    image="ford_fusion.jpg"),
            Vehicle(make="Chevrolet", model="Malibu", year=2022, availability=True, numbers_available=7,
                    image="chevrolet_malibu.jpg"),
            Vehicle(make="Nissan", model="Altima", year=2022, availability=True, numbers_available=6,
                    image="nissan_altima.jpg"),
            # Add more vehicles here
        ]
        db.session.add_all(real_life_vehicles)
        db.session.commit()


if __name__ == '__main__':
    try:
        seed_database()
        print("Database seeded successfully.")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
