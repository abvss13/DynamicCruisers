from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # Relationships
    reviews = db.relationship('Reviews', backref='user', lazy=True)
    likes = db.relationship('Likes', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    vehicles_owned = db.relationship('Vehicle', secondary='user_vehicle', backref='users', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Vehicle(db.Model, SerializerMixin):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    numbers_available = db.Column(db.Integer, nullable=False, default=1)
    likes = db.column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    # Relationships
    dealerships_id = db.relationship('Dealership', secondary='vehicle_dealership', backref='vehicles', lazy=True)
    reviews_id = db.relationship('Reviews', backref='vehicles', lazy=True)

    def __repr__(self):
        return f"Vehicle('{self.make}', '{self.model}', '{self.year}')"
    
class Dealership(db.Model, SerializerMixin):
    __tablename__ = 'dealerships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False) 
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Dealership('{self.name}', '{self.city}', '{self.state}')"
    
class Review (db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user_id = db.relationship('User', backref='reviews', lazy=True)
    vehicle_id = db.relationship('Vehicle', backref='reviews', lazy=True)
    
    
    def __repr__(self):
        return f"Review('{self.title}', '{self.date_posted}')"
    
class Likes (db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    user_id = db.relationship('User', backref='likes', lazy=True)
    vehicle_id = db.relationship('Vehicle', backref='likes', lazy=True)
    
    def __repr__(self):
        return f"Likes('{self.user_id}', '{self.review_id}')"
    
class Rating (db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    # Relationships
    user_id = db.relationship('User', backref='ratings', lazy=True)
    dealership_id = db.relationship('Dealership', backref='ratings', lazy=True)
    
    def __repr__(self):
        return f"Rating('{self.rating}')"
    