from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv,dotenv_values

load_dotenv()
database_path=os.getenv('DATABASE_PATH')
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate=Migrate(app,db)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,unique=True,nullable=False)
    release_date = db.Column(db.Date,nullable=False)
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
       
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': str(self.release_date)
        }

class Actor(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(120),nullable=False)
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender=gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender':self.gender
        }