from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from API import app


db = SQLAlchemy(app)

#-----------------------------------------------SQLALCHEMY MODELS-----------------------------------------------------
#User Models
class User(db.Model):

    __tablename__ = "clients"
    #public_id = db.Column(db.String(50),unique=True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    email = db.Column(db.String(60),primary_key=True)
    password = db.Column(db.String(80),nullable=False)
    user_date_stamp =db.Column(db.String(30),nullable=False)
      
    def __init__(self,username,email, password,user_date_stamp):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password
        self.user_date_stamp = user_date_stamp

    def __repr__(self):
        #method to return user information when querying database
        return "<User: %s>" % self.email

    

class Business(db.Model):
    
    __tablename__ = "Businesses"
    business_id = db.Column(db.String(100), primary_key=True)
    business_title = db.Column(db.String(30))
    business_description = db.Column(db.String(1000))
    category_id =db.Column(db.String(30))
    email = db.Column(db.String(60))
    business_date_stamp = db.Column(db.String(30))
    location_id=db.Column(db.String(30))


    def __init__(self,business_id,business_title,business_description,category_id,email,business_date_stamp,location_id):
        #initiliazing business class constructor
        self.business_id= business_id
        self.business_title = business_title
        self.business_description= business_description
        self.category_id =category_id
        self.email= email
        self.business_date_stamp = business_date_stamp

    def __repr__(self):
        #method for returning data when querying database
        return "<Business: %s>" % self.business_title 


class Review(db.Model):

    __tablename__ = "Reviews"
    username = db.Column(db.String(50),nullable=False)
    review_id = db.Column(db.String(100), primary_key=True)
    review_description = db.Column(db.String(500))
    business_id = db.Column(db.String(100))

    def __init__(self, username, review_id, review_description, business_id):
       #initiliazing business reviews constructor
       self.username=username
       self.review_id= review_id
       self.review_description= review_description
       self.business_id= business_id
    
    def __repr__(self):
        #method for returning data when querying database
        return "<Review: %s>" % self.review_description 