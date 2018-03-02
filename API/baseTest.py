from unittest import TestCase
import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from models import db
from models import User,Business,Review
from app import app


class BaseTestCase(TestCase):
    #setting test database
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresl://postgres:c0m9k#tWxF@localhost/weconnect.db' 

    def setUp(self):
        """ SetUp method .This method is run before each test.It is where all variables for tests are declared 
        and values set. It is important for setting the state your testing for in the application.
        """
        #Declaring testing client
        self.client = app.test_client()
        db.init_app(app)
        db.drop_all()
        db.create_all()

        #Declaring User details  to use for testing
        password="123"
        self.user = {
            "username":"paulus",
            "email":"paulus@gmail.com",
            "password":password
            }
        #hashing the users password for better security
        password_hash = generate_password_hash(password, method='sha256')
        #Saving the users deatils in the database
        user=User("paulus","paulus@gmail.com",password=password_hash,user_date_stamp=str(datetime.datetime.now()))
        db.session.add(user)
        db.session.commit()

        #declaring a sample of invalid data
        self.invalid_data = {}

        #User details for login
        self.user_details = {
            "username":"paulus",
            "password":"123"
        }
        
                
        #Declaring a sample business for testing        
        self.business ={
            "business_title":"rolex", 
            "business_description":"1.Obtain eggs",
            "category_id":"Small",
            "location_id":"Kampala"
            }

        #saving a second sample business in the database
        business=business("1","rolex","1.Obtain eggs","Small","paulus@gmail.com","2017-12-02 13:39:25.892164","Kampala")
        db.session.add(business)
        db.session.commit()
        
        #User details for login and generating a token
        self.user_logins = {
            "username":"paulus",
            "password": "123"
            }
        response = self.client.post("/login", data=json.dumps(self.user_logins),headers={"Content-Type": "application/json"})
        token = json.loads(response.data.decode())["token"]
        self.headers= {"x-access-token": token}
        
    def tearDown(self):
        """ TearDown method.When testing,you want to maintain the state of the application.
        Whenever  the test is run teardown is run after each test so as to restore 
        the original state of the application
        """
        db.session.remove()
        db.drop_all()
 