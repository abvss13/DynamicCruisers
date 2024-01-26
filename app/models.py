from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=True, nullable=False)
    lastname = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    reviews = db.relationship('Review', backref='user', lazy=True)
    likes = db.relationship('Likes', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    vehicles_owned = db.relationship('Vehicle', secondary='user_vehicle', backref='users', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"
    
class Vehicle(db.Model, SerializerMixin):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    availability = db.Column(db.Boolean, nullable=False, default=True)
    numbers_available = db.Column(db.Integer, nullable=False, default=1)

    likes = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    dealerships = db.relationship('Dealership', secondary='vehicle_dealership', backref='vehicles', lazy=True)
    reviews = db.relationship('Review', backref='vehicle', lazy=True)

    def __repr__(self):
        return f"Vehicle('{self.make}', '{self.model}', '{self.year}')"
    
class UserVehicle(db.Model):
    __tablename__ = 'user_vehicle'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    def __repr__(self):
        return f"UserVehicle('{self.user_id}', '{self.vehicle_id}')"
    
class Dealership(db.Model, SerializerMixin):
    __tablename__ = 'dealerships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False) 
    rating = db.Column(db.Float, nullable=False)

    ratings = db.relationship('Rating', backref='dealership', lazy=True)

    def __repr__(self):
        return f"Dealership('{self.name}', '{self.address}', '{self.website}')"
    
class VehicleDealership(db.Model):
    __tablename__ = 'vehicle_dealership'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    dealership_id = db.Column(db.Integer, db.ForeignKey('dealerships.id'), nullable=False)

    def __repr__(self):
        return f"VehicleDealership('{self.vehicle_id}', '{self.dealership_id}')"

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.title}', '{self.date_posted}')"

class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)

    def __repr__(self):
        return f"Likes('{self.user_id}', '{self.review_id}')"

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dealership_id = db.Column(db.Integer, db.ForeignKey('dealerships.id'), nullable=False)
    
    def __repr__(self):
        return f"Rating('{self.rating}')"
